import os
import jwt
from functools import wraps
from flask import request, jsonify

# Secret from env
def get_secret():
    return os.environ.get('JWT_SECRET', 'fallback_secret_for_dev')

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Access denied. No token provided.'}), 401

        token = auth_header.split(' ')[1]
        try:
            decoded = jwt.decode(token, get_secret(), algorithms=['HS256'])
            # Attach user to request via environment or a custom way.
            # Usually in Flask we attach it to Flask's `g` object.
            # But let's attach to request for simplicity similar to req.user
            from flask import g
            g.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired.'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token.'}), 400

        return f(*args, **kwargs)
    return decorated

def authorize(roles=None):
    if roles is None:
        roles = []
        
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import g
            user = getattr(g, 'user', None)
            
            if not user:
                return jsonify({'error': 'Authentication required'}), 401

            if roles and user.get('role') not in roles:
                return jsonify({'error': 'Forbidden: Insufficient permissions'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
