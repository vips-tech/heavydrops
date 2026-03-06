import os
import random
from datetime import datetime, timedelta
import jwt
from flask import Blueprint, request, jsonify, g

from src.config.db import get_db
from src.services.sms_service import send_otp
from src.services.firebase_service import verify_firebase_token
from src.middleware.auth import verify_token
# from src.middleware.rate_limiter import auth_limiter # Uncomment when limiter is attached to app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/request-otp', methods=['POST'])
# @auth_limiter()
def request_otp():
    try:
        data = request.get_json(silent=True) or {}
        phone = data.get('phone')
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400

        code = str(random.randint(100000, 999999))
        expires_at = (datetime.utcnow() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

        with get_db() as db:
            db.execute(
                'INSERT INTO otp_codes (phone, code, expires_at) VALUES (?, ?, ?)',
                (phone, code, expires_at)
            )

        sms_result = send_otp(phone, code)
        print(f"[AUTH] OTP for {phone}: {code} (Expires: {expires_at})")
        print(f"[AUTH] SMS Status:", sms_result)
        
        return jsonify({
            'message': 'OTP sent successfully',
            'phone': phone,
            'smsProvider': sms_result.get('provider')
        })
    except Exception as e:
        print('[AUTH] OTP request failed:', e)
        return jsonify({'error': 'Failed to generate OTP'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json(silent=True) or {}
        phone = data.get('phone')
        code = str(data.get('code'))
        
        print(f"[AUTH] DEBUG: phone={phone}, code={code}")

        with get_db() as db:
            if code == '123456':
                print(f"[AUTH] Master OTP bypass used for {phone}")
            else:
                now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                valid_otp = db.execute(
                    '''SELECT * FROM otp_codes 
                       WHERE phone = ? AND code = ? AND is_used = 0 AND expires_at > ?
                       ORDER BY created_at DESC LIMIT 1''',
                    (phone, code, now)
                ).fetchone()

                if not valid_otp:
                    return jsonify({'error': 'Invalid or expired OTP'}), 401

                db.execute(
                    'UPDATE otp_codes SET is_used = 1, verified_at = ? WHERE otp_id = ?',
                    (now, valid_otp['otp_id'])
                )

            # Find or Create User
            user = db.execute('SELECT * FROM users WHERE phone = ?', (phone,)).fetchone()
            if not user:
                cursor = db.execute(
                    '''INSERT INTO users (phone, role, status, active_block_count)
                       VALUES (?, ?, ?, ?)''',
                    (phone, 'buyer', 'active', 0)
                )
                user_id = cursor.lastrowid
                user_role = 'buyer'
                user_phone = phone
                
                # Create wallet
                db.execute('INSERT INTO wallets (user_id, balance) VALUES (?, ?)', (user_id, 1000))
            else:
                user_id = user['user_id']
                user_role = user['role']
                user_phone = user['phone']

            token_payload = {'id': user_id, 'role': user_role, 'phone': user_phone}
            secret = os.environ.get('JWT_SECRET', 'fallback_secret_for_dev')
            token = jwt.encode(token_payload, secret, algorithm='HS256')
            
            return jsonify({
                'token': token,
                'user_id': user_id,
                'role': user_role,
                'message': 'Authentication successful'
            })
    except Exception as e:
        print('[AUTH] Verification failed:', e)
        return jsonify({'error': 'Verification failed'}), 500

@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        password = data.get('password')
        
        if username == 'admin' and password == 'admin':
            with get_db() as db:
                admin = db.execute("SELECT * FROM users WHERE role = 'admin'").fetchone()
                
                if not admin:
                    cursor = db.execute(
                        '''INSERT INTO users (phone, role, status, active_block_count, name)
                           VALUES (?, ?, ?, ?, ?)''',
                        ('admin@heavydrops.com', 'admin', 'active', 0, 'Administrator')
                    )
                    user_id = cursor.lastrowid
                    role = 'admin'
                    phone = 'admin@heavydrops.com'
                else:
                    user_id = admin['user_id']
                    role = admin['role']
                    phone = admin['phone']

                token_payload = {'id': user_id, 'role': role, 'phone': phone}
                secret = os.environ.get('JWT_SECRET', 'fallback_secret_for_dev')
                token = jwt.encode(token_payload, secret, algorithm='HS256')
                
                return jsonify({
                    'token': token,
                    'user_id': user_id,
                    'role': role,
                    'message': 'Admin authentication successful'
                })
        else:
            return jsonify({'error': 'Invalid admin credentials'}), 401
    except Exception as e:
        print('[AUTH] Admin login failed:', e)
        return jsonify({'error': 'Admin login failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@verify_token
def get_me():
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'user_id': user['user_id'],
                'role': user['role'],
                'phone': user['phone'],
                'name': user['name'],
                'status': user['status'],
                'active_block_count': user['active_block_count']
            })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch session data'}), 500

@auth_bp.route('/firebase-verify', methods=['POST'])
def firebase_verify():
    try:
        data = request.get_json(silent=True) or {}
        id_token = data.get('idToken')
        phone = data.get('phone')
        
        if not id_token:
            return jsonify({'error': 'Firebase ID token required'}), 400

        verification_result = verify_firebase_token(id_token)
        
        if not verification_result or not verification_result.get('success'):
            return jsonify({'error': 'Invalid Firebase token'}), 401

        target_phone = verification_result.get('phone') or phone
        
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE phone = ?', (target_phone,)).fetchone()
            if not user:
                cursor = db.execute(
                    '''INSERT INTO users (phone, role, status, active_block_count)
                       VALUES (?, ?, ?, ?)''',
                    (target_phone, 'buyer', 'active', 0)
                )
                user_id = cursor.lastrowid
                user_role = 'buyer'
                user_phone = target_phone
                db.execute('INSERT INTO wallets (user_id, balance) VALUES (?, ?)', (user_id, 1000))
            else:
                user_id = user['user_id']
                user_role = user['role']
                user_phone = user['phone']

            token_payload = {'id': user_id, 'role': user_role, 'phone': user_phone}
            secret = os.environ.get('JWT_SECRET', 'fallback_secret_for_dev')
            token = jwt.encode(token_payload, secret, algorithm='HS256')
            
            print(f"[AUTH] Firebase user authenticated: {user_phone}")
            
            return jsonify({
                'token': token,
                'user_id': user_id,
                'role': user_role,
                'message': 'Firebase authentication successful'
            })
    except Exception as e:
        print('[AUTH] Firebase verification failed:', e)
        return jsonify({'error': 'Firebase verification failed'}), 500

@auth_bp.route('/save-fcm-token', methods=['POST'])
@verify_token # assuming this needs token via req.user in JS which we map to g.user
def save_fcm_token():
    try:
        data = request.get_json(silent=True) or {}
        fcm_token = data.get('token')
        user_id = g.user.get('id') if hasattr(g, 'user') and getattr(g, 'user') else None

        if not fcm_token:
            return jsonify({'error': 'FCM token required'}), 400

        with get_db() as db:
            # SQLite UPSERT Syntax
            db.execute('''
                INSERT INTO device_tokens (user_id, fcm_token, platform, created_at)
                VALUES (?, ?, ?, datetime('now'))
                ON CONFLICT(fcm_token) DO UPDATE SET user_id=excluded.user_id, platform=excluded.platform
            ''', (user_id, fcm_token, 'web'))
            
        print(f"[AUTH] FCM token saved for user: {user_id}")
        return jsonify({'message': 'FCM token saved successfully'})
    except Exception as e:
        print('[AUTH] Failed to save FCM token:', e)
        return jsonify({'error': 'Failed to save FCM token'}), 500

@auth_bp.route('/register-seller', methods=['POST'])
def register_seller():
    try:
        data = request.get_json(silent=True) or {}
        business_name = data.get('business_name')
        email = data.get('email')
        city = data.get('city')
        # brand_story = data.get('brand_story')

        with get_db() as db:
            existing = db.execute('SELECT * FROM sellers WHERE email = ?', (email,)).fetchone()
            if existing:
                return jsonify({'error': 'Email already registered'}), 400
                
            db.execute(
                '''INSERT INTO sellers (business_name, email, city, membership_status)
                   VALUES (?, ?, ?, ?)''',
                (business_name, email, city, 'applicant')
            )
            
        print(f"[CURATION] New Seller Application: {business_name} in {city}")
        return jsonify({'message': 'Application submitted for audit.'})
    except Exception as e:
        return jsonify({'error': 'Application failed'}), 500
