import os
from datetime import datetime
from flask import Blueprint, jsonify, request, g
from werkzeug.utils import secure_filename
from src.config.db import get_db
from src.middleware.auth import verify_token, authorize
from src.services.trust_service import penalize_no_show

seller_bp = Blueprint('seller', __name__)

@seller_bp.route('/profile/<int:seller_id>', methods=['GET'])
def get_seller_profile(seller_id):
    try:
        with get_db() as db:
            seller = db.execute('SELECT * FROM sellers WHERE seller_id = ?', (seller_id,)).fetchone()
            if not seller:
                return jsonify({'error': 'Seller not found'}), 404

            designs = db.execute('''
                SELECT * FROM designs 
                WHERE seller_id = ? AND availability_status = 'available'
            ''', (seller_id,)).fetchall()

            result = dict(seller)
            result['collection'] = [dict(d) for d in designs]
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch seller profile'}), 500

@seller_bp.route('/me', methods=['GET'])
@verify_token
@authorize(['seller', 'admin'])
def get_my_seller_profile():
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            seller = db.execute('SELECT * FROM sellers WHERE user_id = ?', (user_id,)).fetchone()
            if not seller:
                return jsonify({'error': 'No seller profile associated with this account.'}), 404
            return jsonify(dict(seller))
    except Exception as e:
        return jsonify({'error': 'Failed to fetch your seller profile'}), 500

@seller_bp.route('/dashboard/<int:seller_id>', methods=['GET'])
@verify_token
@authorize(['seller', 'admin'])
def get_dashboard_data(seller_id):
    try:
        with get_db() as db:
            active_blocks = db.execute('''
                SELECT b.*, d.category, d.purity
                FROM blocks b
                JOIN designs d ON b.design_id = d.design_id
                WHERE d.seller_id = ? AND b.status = 'active'
            ''', (seller_id,)).fetchall()

            appointments = db.execute('''
                SELECT a.*, u.phone
                FROM appointments a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.seller_id = ?
            ''', (seller_id,)).fetchall()

            design_stats = db.execute('''
                SELECT SUM(view_count) as total_views, COUNT(design_id) as total_designs
                FROM designs WHERE seller_id = ?
            ''', (seller_id,)).fetchone()

            total_likes = db.execute('''
                SELECTCOUNT(*) as count
                FROM likes l
                JOIN designs d ON l.design_id = d.design_id
                WHERE d.seller_id = ?
            ''', (seller_id,)).fetchone()

            anonymized_appts = []
            pending_appts = 0
            for a in appointments:
                appt_dict = dict(a)
                appt_dict['phone'] = '******' + appt_dict['phone'][-4:]
                if appt_dict['status'] == 'requested':
                    pending_appts += 1
                anonymized_appts.append(appt_dict)

            return jsonify({
                'metrics': {
                    'total_views': int(design_stats['total_views']) if design_stats and design_stats['total_views'] else 0,
                    'total_likes': int(total_likes['count']) if total_likes else 0,
                    'total_active_intent': len(active_blocks),
                    'pending_appointments': pending_appts
                },
                'blocks': [dict(b) for b in active_blocks],
                'appointments': anonymized_appts
            })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500

@seller_bp.route('/performance/<int:seller_id>', methods=['GET'])
@verify_token
@authorize(['seller', 'admin'])
def get_design_performance(seller_id):
    try:
        with get_db() as db:
            designs = db.execute('''
                SELECT design_id, category, purity, view_count, availability_status
                FROM designs WHERE seller_id = ?
            ''', (seller_id,)).fetchall()

            performance_data = []
            for d in designs:
                likes_count = db.execute('SELECT COUNT(*) as count FROM likes WHERE design_id = ?', (d['design_id'],)).fetchone()
                blocks_count = db.execute('SELECT COUNT(*) as count FROM blocks WHERE design_id = ?', (d['design_id'],)).fetchone()
                
                perf = dict(d)
                perf['likes'] = int(likes_count['count']) if likes_count else 0
                perf['blocks'] = int(blocks_count['count']) if blocks_count else 0
                performance_data.append(perf)

            return jsonify(performance_data)
    except Exception as e:
        print('[SELLER] Performance fetch failed:', e)
        return jsonify({'error': 'Failed to fetch performance data'}), 500

@seller_bp.route('/appointments/<int:appointment_id>/outcome', methods=['POST'])
@verify_token
@authorize(['seller', 'admin'])
def mark_appointment_outcome(appointment_id):
    try:
        data = request.get_json(silent=True) or {}
        outcome = data.get('outcome')
        if outcome not in ['attended', 'no-show']:
            return jsonify({'error': 'Invalid outcome'}), 400

        with get_db() as db:
            appt = db.execute('SELECT * FROM appointments WHERE appointment_id = ?', (appointment_id,)).fetchone()
            if not appt:
                return jsonify({'error': 'Appointment not found'}), 404

            db.execute('''
                UPDATE appointments SET status = ?, seller_notes = ?
                WHERE appointment_id = ?
            ''', ('attended' if outcome == 'attended' else 'no_show', outcome, appointment_id))

            if outcome == 'attended':
                db.execute("UPDATE blocks SET status = 'converted' WHERE block_id = ?", (appt['block_id'],))
                db.execute("UPDATE designs SET availability_status = 'sold' WHERE design_id = ?", (appt['design_id'],))

            if outcome == 'no-show':
                penalize_no_show(appt['user_id'], appt['block_id'], db)

            return jsonify({'message': f'Outcome marked as {outcome}'})
    except Exception as e:
        return jsonify({'error': f'Failed to mark outcome: {str(e)}'}), 500

@seller_bp.route('/designs/<int:design_id>', methods=['PATCH'])
@verify_token
@authorize(['seller', 'admin'])
def update_design(design_id):
    try:
        updates = request.get_json(silent=True) or {}
        
        with get_db() as db:
            design = db.execute('SELECT * FROM designs WHERE design_id = ?', (design_id,)).fetchone()
            if not design:
                return jsonify({'error': 'Design not found'}), 404

            if design['availability_status'] == 'blocked' and ('gold_rate_snapshot' in updates or 'making_charge_snapshot' in updates):
                return jsonify({'error': 'SELLER SYSTEM BREACH: Price modification forbidden during active intent block.'}), 403

            # Update fields safely. In a real app we'd validate the keys from updates via a schema.
            allowed_keys = ['category', 'purity', 'weight', 'making_charge_snapshot', 'gold_rate_snapshot', 'occasion_tag']
            updates_to_make = {k: v for k, v in updates.items() if k in allowed_keys}
            
            if updates_to_make:
                set_clause = ', '.join([f"{k} = ?" for k in updates_to_make.keys()])
                values = list(updates_to_make.values())
                values.append(design_id)
                db.execute(f"UPDATE designs SET {set_clause} WHERE design_id = ?", tuple(values))

            return jsonify({'message': 'Design updated successfully'})
    except Exception as e:
        return jsonify({'error': 'Update failed'}), 500

@seller_bp.route('/designs/<int:design_id>/media', methods=['POST'])
@verify_token
@authorize(['seller'])
def upload_design_media(design_id):
    try:
        shot_type = request.form.get('shot_type', 'master')
        user_id = g.user.get('id')
        
        if 'images' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
            
        files = request.files.getlist('images')
        if not files or len(files) == 0:
            return jsonify({'error': 'No files uploaded'}), 400

        with get_db() as db:
            design = db.execute('''
                SELECT d.*, s.user_id as seller_user_id
                FROM designs d
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE d.design_id = ?
            ''', (design_id,)).fetchone()

            if not design:
                return jsonify({'error': 'Design not found'}), 404

            if design['seller_user_id'] != user_id:
                print(f"[SECURITY] Cross-seller upload attempt detected. User #{user_id} tried to upload to Design #{design_id}")
                return jsonify({'error': 'Unauthorized: You do not own this design'}), 403

            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            upload_dir = os.path.join(base_dir, 'uploads', 'designs')
            os.makedirs(upload_dir, exist_ok=True)

            media_entries = []
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    # To avoid overwrite, we can prepend timestamp
                    filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    
                    media_entries.append((
                        design_id,
                        f"/uploads/designs/{filename}",
                        'image',
                        shot_type,
                        'pending_review'
                    ))

            if media_entries:
                db.executemany('''
                    INSERT INTO design_media (design_id, uri, media_type, shot_type, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', media_entries)

                now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                db.execute('''
                    UPDATE designs SET media_quality_status = 'pending', updated_at = ?
                    WHERE design_id = ?
                ''', (now, design_id))

            return jsonify({
                'message': 'Photography uploaded and pending review.',
                'count': len(media_entries)
            }), 201

    except Exception as e:
        print('[PHOTOGRAPHY] Upload failed:', e)
        return jsonify({'error': 'Upload infrastructure failure'}), 500
