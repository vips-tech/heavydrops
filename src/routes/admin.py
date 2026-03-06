from datetime import datetime
import time
from flask import Blueprint, jsonify, request, g
from src.config.db import get_db
from src.services.queue_service import queue_service
from src.middleware.auth import verify_token, authorize
from src.middleware.pilot_guard import seller_cap_guard

admin_bp = Blueprint('admin', __name__)

def log_admin_action(admin_id, action, target_entity, target_id, description, db_conn):
    db_conn.execute('''
        INSERT INTO admin_logs (admin_id, action, target_entity, target_id, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (admin_id, action, target_entity, target_id, description))

# Apply Global Admin Gating to all routes in this blueprint
@admin_bp.before_request
@verify_token
@authorize(['admin'])
def require_admin():
    pass

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        with get_db() as db:
            users = db.execute('SELECT COUNT(*) as count FROM users').fetchone()
            sellers = db.execute('SELECT COUNT(*) as count FROM sellers').fetchone()
            blocks = db.execute("SELECT COUNT(*) as count FROM blocks WHERE status = 'active'").fetchone()
            wallet = db.execute('SELECT SUM(balance) as total FROM wallets').fetchone()

            return jsonify({
                'users': int(users['count']) if users else 0,
                'sellers': int(sellers['count']) if sellers else 0,
                'active_intent_blocks': int(blocks['count']) if blocks else 0,
                'platform_wallet_balance': float(wallet['total']) if wallet and wallet['total'] else 0.0
            })
    except Exception as e:
        print('[ADMIN] Error getting stats:', e)
        return jsonify({'error': 'Failed to fetch admin stats'}), 500

@admin_bp.route('/wallet/adjust', methods=['POST'])
def adjust_wallet():
    try:
        data = request.get_json(silent=True) or {}
        user_id = data.get('user_id')
        amount = float(data.get('amount', 0))
        reason = data.get('reason')
        admin_id = g.user.get('id')
        
        if not user_id or not amount or not reason or len(reason) < 5:
            return jsonify({'error': 'Invalid parameters'}), 400

        cycle_ref = f"ADM-{str(int(time.time()*1000))[-9:].upper()}"

        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            if not wallet:
                return jsonify({'error': 'Wallet not found'}), 404

            new_balance = wallet['balance'] + amount
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            db.execute('UPDATE wallets SET balance = ?, last_updated = ? WHERE user_id = ?', 
                      (new_balance, now, user_id))
            
            t_type = 'credit' if amount > 0 else 'debit'
            db.execute('''
                INSERT INTO wallet_transactions (wallet_id, amount, type, source_type, description, reference_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (wallet['wallet_id'], amount, t_type, 'correction', reason, cycle_ref))

            log_admin_action(admin_id, 'adjust_wallet', 'user', user_id, 
                            f"Adjusted by {amount}. Reason: {reason}. Ref: {cycle_ref}", db)

            return jsonify({'message': 'Wallet adjusted successfully'})
            
    except Exception as e:
        print('[ADMIN] Error adjusting wallet:', e)
        return jsonify({'error': 'Failed to adjust wallet'}), 500

@admin_bp.route('/users', methods=['GET'])
def get_users():
    try:
        with get_db() as db:
            users = db.execute('''
                SELECT u.*, w.balance 
                FROM users u
                LEFT JOIN wallets w ON u.user_id = w.user_id
            ''').fetchall()
            return jsonify([dict(u) for u in users])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users'}), 500

@admin_bp.route('/users/<int:user_id>/status', methods=['PATCH'])
def update_user_status(user_id):
    try:
        data = request.get_json(silent=True) or {}
        status = data.get('status')
        if status not in ['active', 'restricted', 'suspended']:
            return jsonify({'error': 'Invalid status'}), 400

        role_map = {'suspended': 'visitor', 'active': 'buyer', 'restricted': 'restricted'}
        role = role_map[status]
        admin_id = g.user.get('id')

        with get_db() as db:
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            db.execute('UPDATE users SET role = ?, status = ?, updated_at = ? WHERE user_id = ?', 
                      (role, status, now, user_id))
            
            log_admin_action(admin_id, 'update_user_status', 'user', user_id, 
                            f"Status set to {status}", db)

            return jsonify({'message': f'User status updated to {status}'})
            
    except Exception as e:
        return jsonify({'error': 'Failed to update user status'}), 500

@admin_bp.route('/appointments', methods=['GET'])
def get_appointments_summary():
    try:
        with get_db() as db:
            appointments = db.execute('''
                SELECT a.*, u.phone as buyer_phone, s.business_name as seller_brand, b.status as block_current_status
                FROM appointments a
                JOIN users u ON a.user_id = u.user_id
                JOIN sellers s ON a.seller_id = s.seller_id
                JOIN blocks b ON a.block_id = b.block_id
                ORDER BY a.appointment_time DESC
            ''').fetchall()
            return jsonify([dict(a) for a in appointments])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch appointment patterns'}), 500

@admin_bp.route('/blocks', methods=['GET'])
def get_all_blocks():
    try:
        with get_db() as db:
            blocks = db.execute('''
                SELECT b.*, u.phone, d.category
                FROM blocks b
                JOIN users u ON b.user_id = u.user_id
                JOIN designs d ON b.design_id = d.design_id
            ''').fetchall()
            return jsonify([dict(b) for b in blocks])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch all blocks'}), 500

@admin_bp.route('/violations', methods=['POST'])
def log_violation():
    try:
        data = request.get_json(silent=True) or {}
        entity_type = data.get('entity_type')
        entity_id = data.get('entity_id')
        v_type = data.get('type')
        reason = data.get('reason')
        level = data.get('level', 'warning')

        with get_db() as db:
            db.execute('''
                INSERT INTO violations (entity_type, entity_id, type, reason, level)
                VALUES (?, ?, ?, ?, ?)
            ''', (entity_type, entity_id, v_type, reason, level))

            if entity_type == 'buyer' and level == 'strike':
                db.execute('UPDATE users SET strike_count = strike_count + 1 WHERE user_id = ?', (entity_id,))

            if entity_type == 'seller':
                queue_service.publish('seller.violation', {
                    'user_id': entity_id,
                    'type': v_type,
                    'reason': reason
                }, db)

            return jsonify({'message': 'Violation recorded successfully'}), 201
            
    except Exception as e:
        return jsonify({'error': 'Failed to log violation'}), 500

@admin_bp.route('/violations', methods=['GET'])
def get_violations():
    try:
        with get_db() as db:
            violations = db.execute('SELECT * FROM violations ORDER BY created_at DESC').fetchall()
            return jsonify([dict(v) for v in violations])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch violation history'}), 500

@admin_bp.route('/designs/pending', methods=['GET'])
def get_pending_designs():
    try:
        with get_db() as db:
            designs = db.execute('''
                SELECT DISTINCT d.*, s.business_name
                FROM designs d
                JOIN sellers s ON d.seller_id = s.seller_id
                LEFT JOIN design_media m ON d.design_id = m.design_id
                WHERE d.media_quality_status = 'pending' OR m.status = 'pending_review'
            ''').fetchall()
            return jsonify([dict(d) for d in designs])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch pending designs'}), 500

@admin_bp.route('/designs/<int:design_id>/approve', methods=['PATCH'])
def approve_listing(design_id):
    try:
        data = request.get_json(silent=True) or {}
        status = data.get('status')
        if status not in ['approved', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400

        admin_id = g.user.get('id')

        with get_db() as db:
            availability = 'available' if status == 'approved' else 'rejected'
            db.execute('''
                UPDATE designs SET media_quality_status = ?, availability_status = ? 
                WHERE design_id = ?
            ''', (status, availability, design_id))
            
            log_admin_action(admin_id, 'approve_listing', 'design', design_id, 
                            f"Photography audit: {status}", db)

            return jsonify({'message': f'Photography Audit: Listing {status}'})

    except Exception as e:
        return jsonify({'error': 'Failed to approve listing'}), 500

@admin_bp.route('/designs/media/pending', methods=['GET'])
def get_pending_media():
    try:
        with get_db() as db:
            media = db.execute('''
                SELECT m.*, s.business_name, d.category
                FROM design_media m
                JOIN designs d ON m.design_id = d.design_id
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE m.status = 'pending_review'
            ''').fetchall()
            return jsonify([dict(m) for m in media])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch pending media'}), 500

@admin_bp.route('/designs/media/<int:media_id>/review', methods=['POST'])
def review_design_media(media_id):
    try:
        data = request.get_json(silent=True) or {}
        status = data.get('status')
        reason = data.get('reason', '')
        if status not in ['approved', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400

        admin_id = g.user.get('id')

        with get_db() as db:
            media = db.execute('SELECT * FROM design_media WHERE media_id = ?', (media_id,)).fetchone()
            if not media:
                return jsonify({'error': 'Media entry not found'}), 404

            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            db.execute('UPDATE design_media SET status = ?, updated_at = ? WHERE media_id = ?', 
                      (status, now, media_id))
            
            log_admin_action(admin_id, 'review_media', 'design_media', media_id, 
                            f"Photography review: {status}. {reason}", db)

            if status == 'approved' and media['shot_type'] == 'master':
                db.execute('''
                    UPDATE designs SET media_quality_status = 'approved', availability_status = 'available'
                    WHERE design_id = ?
                ''', (media['design_id'],))
                
            if status == 'rejected':
                remaining = db.execute('''
                    SELECT COUNT(*) as count FROM design_media 
                    WHERE design_id = ? AND status = 'approved'
                ''', (media['design_id'],)).fetchone()
                
                if int(remaining['count']) == 0:
                    db.execute('''
                        UPDATE designs SET media_quality_status = 'rejected', availability_status = 'rejected'
                        WHERE design_id = ?
                    ''', (media['design_id'],))

            return jsonify({'message': f'Media review: {status}'})
            
    except Exception as e:
        return jsonify({'error': 'Failed to review media'}), 500

@admin_bp.route('/sellers', methods=['GET'])
def get_sellers():
    try:
        status = request.args.get('status')
        with get_db() as db:
            if status:
                sellers = db.execute('SELECT * FROM sellers WHERE membership_status = ?', (status,)).fetchall()
            else:
                sellers = db.execute('SELECT * FROM sellers').fetchall()
            return jsonify([dict(s) for s in sellers])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch sellers'}), 500

@admin_bp.route('/sellers/<int:seller_id>/status', methods=['PATCH'])
@seller_cap_guard
def update_seller_status(seller_id):
    try:
        data = request.get_json(silent=True) or {}
        status = data.get('status')
        if status not in ['active', 'suspended', 'applicant']:
            return jsonify({'error': 'Invalid status'}), 400

        admin_id = g.user.get('id')

        with get_db() as db:
            db.execute('UPDATE sellers SET membership_status = ? WHERE seller_id = ?', 
                      (status, seller_id))
            
            log_admin_action(admin_id, 'update_seller_status', 'seller', seller_id, 
                            f"Status set to {status}", db)

            return jsonify({'message': f'Seller status updated to {status}'})
            
    except Exception as e:
        return jsonify({'error': 'Failed to update seller status'}), 500

@admin_bp.route('/gold-rate', methods=['GET'])
def get_gold_rate():
    try:
        with get_db() as db:
            rates = db.execute('''
                SELECT * FROM gold_rates 
                WHERE purity IN ('22K', '24K') 
                ORDER BY updated_at DESC
            ''').fetchall()
            
            latest = {}
            for r in rates:
                if r['purity'] not in latest:
                    latest[r['purity']] = dict(r)
                    
            return jsonify(latest)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch gold rates'}), 500

@admin_bp.route('/gold-rate', methods=['POST'])
def update_gold_rate():
    try:
        data = request.get_json(silent=True) or {}
        purity = data.get('purity')
        rate = float(data.get('rate', 0))
        
        if purity not in ['22K', '24K'] or rate <= 0:
            return jsonify({'error': 'Invalid purity or rate'}), 400

        admin_id = g.user.get('id')

        with get_db() as db:
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            db.execute('''
                INSERT INTO gold_rates (purity, rate_per_gram, updated_at)
                VALUES (?, ?, ?)
            ''', (purity, rate, now))
            
            log_admin_action(admin_id, 'update_gold_rate', 'gold_rates', purity, 
                            f"Updated {purity} rate to ₹{rate}", db)

            return jsonify({'message': f'Gold rate for {purity} updated to ₹{rate}'})
            
    except Exception as e:
        return jsonify({'error': 'Failed to update gold rate'}), 500
