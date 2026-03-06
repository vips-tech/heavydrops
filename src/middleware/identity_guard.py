from functools import wraps
from flask import request, jsonify, g
from datetime import datetime, timedelta
from src.config.db import get_db

def identity_guard(f):
    """
    Identity Guard: Enforces fresh OTP verification for critical actions.
    Requirements: User must have verified an OTP in the last 15 minutes.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user = getattr(g, 'user', None)
        if hasattr(user, 'get'):
            user_id = user.get('id')
            phone = user.get('phone')
        else:
            return jsonify({'error': 'Security guard failure'}), 500

        try:
            with get_db() as db:
                if not phone:
                    # Fetch from db
                    db_user = db.execute('SELECT phone FROM users WHERE user_id = ?', (user_id,)).fetchone()
                    if db_user:
                        phone = db_user['phone']

                if not phone:
                    return jsonify({'error': 'Identity verification failed: Phone not found.'}), 401
                
                fifteen_mins_ago = (datetime.utcnow() - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')

                # Check fresh OTP
                fresh_otp = db.execute(
                    '''SELECT * FROM otp_codes 
                       WHERE phone = ? AND is_used = 1 AND verified_at >= ?''',
                    (phone, fifteen_mins_ago)
                ).fetchone()

                if not fresh_otp:
                    return jsonify({
                        'error': 'Identity Refresh Required',
                        'message': 'For your security, please verify a fresh OTP before performing this action.'
                    }), 403

        except Exception as e:
            print(f"[IDENTITY GUARD] Error: {e}")
            return jsonify({'error': 'Security guard failure'}), 500

        return f(*args, **kwargs)
    return decorated
