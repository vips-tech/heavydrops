from datetime import datetime
from flask import Blueprint, jsonify, g
from src.config.db import get_db
from src.middleware.auth import verify_token

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/', methods=['GET'])
@verify_token
def get_wallet_info():
    try:
        user_id = g.user.get('id')
        
        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
            
            if not wallet:
                return jsonify({'error': 'Wallet not found'}), 404
                
            active_blocks = db.execute(
                "SELECT COUNT(*) as count FROM blocks WHERE user_id = ? AND status = 'active'", 
                (user_id,)
            ).fetchone()
            
            is_expired = False
            if wallet['expiry_date']:
                # The DB expiry_date is usually timestamp string. Make sure we parse or compare safely.
                expiry = datetime.strptime(wallet['expiry_date'], '%Y-%m-%d %H:%M:%S') if type(wallet['expiry_date']) == str else wallet['expiry_date']
                if expiry < datetime.utcnow(): 
                    is_expired = True

            strike_count = user.get('strike_count') or 0
            status_display = 'Good Standing' if user['status'] == 'active' else 'Restricted'

            return jsonify({
                'balance': wallet['balance'],
                'expiry_date': wallet['expiry_date'],
                'is_expired': is_expired,
                'active_blocks_count': int(active_blocks['count']) if active_blocks else 0,
                'strike_count': strike_count,
                'status': status_display,
                'is_verified': True
            })
            
    except Exception as e:
        print('[WALLET] Error fetching info:', e)
        return jsonify({'error': 'Failed to fetch wallet info'}), 500

@wallet_bp.route('/transactions', methods=['GET'])
@verify_token
def get_ledger():
    try:
        user_id = g.user.get('id')
        
        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            if not wallet:
                return jsonify({'error': 'Wallet not found'}), 404
                
            transactions = db.execute(
                'SELECT * FROM wallet_transactions WHERE wallet_id = ? ORDER BY created_at DESC', 
                (wallet['wallet_id'],)
            ).fetchall()
            
            # Since sqlite fetchall with dict_factory returns list of dicts, we can directly return
            return jsonify(transactions)
            
    except Exception as e:
        print('[WALLET] Error fetching ledger:', e)
        return jsonify({'error': 'Failed to fetch transaction ledger'}), 500
