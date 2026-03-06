from datetime import datetime
from flask import Blueprint, jsonify, request, g
from src.config.db import get_db
from src.services.queue_service import queue_service
from src.services.trust_service import penalize_no_show
from src.middleware.auth import verify_token
from src.middleware.identity_guard import identity_guard
from src.middleware.maintenance_mode import maintenance_gate
# from src.middleware.rate_limiter import bridge_limiter

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['POST'])
@verify_token
# @bridge_limiter()
@maintenance_gate
@identity_guard
def book_appointment():
    try:
        data = request.get_json(silent=True) or {}
        block_id = data.get('block_id')
        appointment_time = data.get('appointment_time')
        liability_accepted = bool(data.get('liability_accepted', False))
        
        if not block_id or not appointment_time:
            return jsonify({'error': 'block_id and appointment_time are required'}), 400

        user_id = g.user.get('id')

        with get_db() as db:
            block = db.execute('''
                SELECT b.*, d.seller_id 
                FROM blocks b
                JOIN designs d ON b.design_id = d.design_id
                WHERE b.block_id = ? AND b.user_id = ? AND b.status = 'active'
            ''', (block_id, user_id)).fetchone()

            if not block:
                return jsonify({'error': 'Cannot book appointment. No active intent block found for this design.'}), 400

            existing = db.execute('''
                SELECT * FROM appointments
                WHERE block_id = ? AND status IN ('requested', 'confirmed')
            ''', (block_id,)).fetchone()

            if existing:
                return jsonify({'error': 'An appointment is already linked to this intent block.'}), 400

            cursor = db.execute('''
                INSERT INTO appointments (user_id, seller_id, block_id, appointment_time, status, liability_accepted)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, block['seller_id'], block_id, appointment_time, 'requested', liability_accepted))
            appointment_id = cursor.lastrowid

            queue_service.publish('appointment.booked', {
                'user_id': user_id,
                'design_id': block['design_id'],
                'time': appointment_time
            }, db)

            return jsonify({
                'message': 'Appointment requested successfully',
                'appointment_id': appointment_id
            }), 201

    except Exception as e:
        print('[BRIDGE] Booking failed:', e)
        return jsonify({'error': 'Failed to create appointment'}), 500

@appointment_bp.route('/<int:appointment_id>/status', methods=['PATCH'])
@verify_token
@maintenance_gate
def update_appointment_status(appointment_id):
    print(f"[DEBUG] updateAppointmentStatus Called. Params: {appointment_id}, Body: {request.get_json(silent=True)}")
    try:
        data = request.get_json(silent=True) or {}
        status = data.get('status')
        valid_statuses = ['confirmed', 'attended', 'no_show', 'cancelled']
        
        if status not in valid_statuses:
            return jsonify({'error': 'Invalid status update'}), 400

        with get_db() as db:
            appt = db.execute('SELECT * FROM appointments WHERE appointment_id = ?', (appointment_id,)).fetchone()
            if not appt:
                return jsonify({'error': 'Appointment not found'}), 404

            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            db.execute('''
                UPDATE appointments SET status = ?, updated_at = ?
                WHERE appointment_id = ?
            ''', (status, now, appointment_id))

            print(f"[DEBUG] Status identified: {status}")
            
            if status == 'attended':
                print(f"[DEBUG] Converting block #{appt['block_id']}")
                db.execute("UPDATE blocks SET status = 'converted' WHERE block_id = ?", (appt['block_id'],))
            
            elif status == 'no_show':
                print(f"[DEBUG] Triggering penalizeNoShow for User #{appt['user_id']}")
                penalize_no_show(appt['user_id'], appt['block_id'], db)
                
                queue_service.publish('appointment.no_show', {
                    'user_id': appt['user_id'],
                    'design_id': appt['design_id'],
                    'appointment_id': appt['appointment_id']
                }, db)

            return jsonify({'message': f'Appointment status updated to {status}'})

    except Exception as e:
        print('[BRIDGE] Status update failed:', e)
        return jsonify({'error': str(e)}), 400
