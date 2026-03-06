from datetime import datetime
from flask import Blueprint, jsonify
from src.config.db import get_db
from src.middleware.auth import verify_token, authorize
from src.config.pilot_config import PILOT_MODE, PILOT_CONSTRAINTS, FEATURES

health_bp = Blueprint('health', __name__)

@health_bp.route('/telemetry', methods=['GET'])
@verify_token
@authorize(['admin'])
def get_system_health():
    try:
        with get_db() as db:
            active_blocks = db.execute("SELECT COUNT(*) as count FROM blocks WHERE status = 'active'").fetchone()
            converted_blocks = db.execute("SELECT COUNT(*) as count FROM blocks WHERE status = 'converted'").fetchone()
            wallet_total = db.execute('SELECT SUM(balance) as total FROM wallets').fetchone()
            total_strikes = db.execute('SELECT SUM(strike_count) as total FROM users').fetchone()
            pending_listings = db.execute("SELECT COUNT(*) as count FROM designs WHERE media_quality_status = 'pending'").fetchone()

            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'metrics': {
                    'active_blocks': int(active_blocks['count']) if active_blocks else 0,
                    'conversion_count': int(converted_blocks['count']) if converted_blocks else 0,
                    'total_platform_wallet': float(wallet_total['total']) if wallet_total and wallet_total['total'] else 0.0,
                    'curation_backlog': int(pending_listings['count']) if pending_listings else 0,
                    'abuse_signals': {
                        'total_strikes': int(total_strikes['total']) if total_strikes and total_strikes['total'] else 0
                    }
                }
            })
    except Exception as e:
        print('[HEALTH] Telemetry failed:', e)
        return jsonify({'error': 'Failed to retrieve system health'}), 500

@health_bp.route('/config', methods=['GET'])
def get_system_config():
    return jsonify({
        'pilot_mode': PILOT_MODE,
        'features': FEATURES,
        'constraints': PILOT_CONSTRAINTS if PILOT_MODE else None
    })
