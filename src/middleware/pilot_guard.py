from functools import wraps
from flask import request, jsonify
from src.config.pilot_config import PILOT_MODE, PILOT_CONSTRAINTS
from src.config.db import get_db

def seller_cap_guard(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not PILOT_MODE:
            return f(*args, **kwargs)

        try:
            with get_db() as db:
                count_result = db.execute('SELECT COUNT(seller_id) as count FROM sellers').fetchone()
                if count_result and count_result['count'] >= PILOT_CONSTRAINTS['MAX_SELLERS']:
                    return jsonify({
                        'error': 'Pilot Limit Reached',
                        'message': f"The platform is currently limited to {PILOT_CONSTRAINTS['MAX_SELLERS']} curated sellers during the pilot phase."
                    }), 403
        except Exception as e:
            print(f"[PILOT GUARD] Error checking seller cap: {e}")
            return jsonify({'error': 'Server error'}), 500

        return f(*args, **kwargs)
    return decorated

def geo_lock_guard(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not PILOT_MODE:
            return f(*args, **kwargs)

        data = request.get_json(silent=True) or {}
        city = data.get('city')
        if city and city != PILOT_CONSTRAINTS['RESTRICTED_CITY']:
            return jsonify({
                'error': 'Restricted Geography',
                'message': f"During pilot, discovery is limited to {PILOT_CONSTRAINTS['RESTRICTED_CITY']}."
            }), 403
            
        return f(*args, **kwargs)
    return decorated

def onboarding_guard(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if PILOT_MODE and not PILOT_CONSTRAINTS['ALLOW_SELF_ONBOARDING']:
            return jsonify({
                'error': 'Invite Required',
                'message': 'Self-onboarding is disabled during pilot. Please contact platform admin.'
            }), 403
            
        return f(*args, **kwargs)
    return decorated
