from functools import wraps
from flask import jsonify

IS_MAINTENANCE_MODE = False

def set_maintenance_mode(status: bool):
    global IS_MAINTENANCE_MODE
    IS_MAINTENANCE_MODE = status
    print(f"[SYSTEM] Maintenance Mode: {'ENABLED' if status else 'DISABLED'}")

def maintenance_gate(f):
    """
    Middleware to block requests if maintenance is active
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if IS_MAINTENANCE_MODE:
            return jsonify({
                'error': 'Platform Emergency Freeze Active',
                'message': 'System is undergoing data integrity restoration. Intent signaling is temporarily disabled.',
                'status': 'maintenance'
            }), 503
        return f(*args, **kwargs)
    return decorated
