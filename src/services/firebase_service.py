import os
import firebase_admin
from firebase_admin import credentials, messaging, auth

_firebase_app = None

def initialize_firebase():
    global _firebase_app
    if _firebase_app:
        return _firebase_app

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        sa_path = os.path.join(base_dir, 'firebase-service-account.json')
        
        if os.path.exists(sa_path):
            cred = credentials.Certificate(sa_path)
            _firebase_app = firebase_admin.initialize_app(cred, {
                'projectId': 'login-otp-29372'
            })
            print('[FIREBASE] Admin SDK initialized successfully')
            return _firebase_app
        else:
            print('[FIREBASE] Service account file not found')
            return None
    except Exception as e:
        print(f'[FIREBASE] Failed to initialize Admin SDK: {str(e)}')
        return None

def send_otp_via_push(device_token, otp, phone):
    app = initialize_firebase()
    if not app:
        raise ValueError('Firebase not initialized')
        
    try:
        import time
        message = messaging.Message(
            notification=messaging.Notification(
                title='Heavy Drops - Verification Code',
                body=f"Your OTP is: {otp}. Valid for 5 minutes."
            ),
            data={
                'otp': str(otp),
                'phone': phone,
                'type': 'otp_verification',
                'timestamp': str(int(time.time() * 1000))
            },
            token=device_token
        )
        response = messaging.send(message)
        print(f"[FIREBASE] Push notification sent successfully: {response}")
        return {'success': True, 'provider': 'firebase-push', 'messageId': response}
    except Exception as e:
        print(f'[FIREBASE] Push notification failed: {str(e)}')
        raise e

def verify_firebase_token(id_token):
    app = initialize_firebase()
    if not app:
        raise ValueError('Firebase not initialized')
        
    try:
        decoded_token = auth.verify_id_token(id_token)
        print(f"[FIREBASE] Token verified for user: {decoded_token['uid']}")
        return {
            'success': True,
            'uid': decoded_token['uid'],
            'phone': decoded_token.get('phone_number'),
            'email': decoded_token.get('email')
        }
    except Exception as e:
        print(f'[FIREBASE] Token verification failed: {str(e)}')
        raise e
