from flask import Blueprint, jsonify, request, g
from src.config.db import get_db
from src.services.block_service import create_block
from src.middleware.auth import verify_token
from src.middleware.identity_guard import identity_guard
from src.middleware.maintenance_mode import maintenance_gate
# from src.middleware.rate_limiter import intent_limiter # Uncomment when limiter is attached to app

intent_bp = Blueprint('intent', __name__)

@intent_bp.route('/me/active', methods=['GET'])
@verify_token
def get_my_active_blocks():
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            blocks = db.execute('''
                SELECT b.*, d.category, d.purity, d.seller_id, d.title
                FROM blocks b
                JOIN designs d ON b.design_id = d.design_id
                WHERE b.user_id = ? AND b.status = 'active'
            ''', (user_id,)).fetchall()
            
            return jsonify([dict(b) for b in blocks])
    except Exception as e:
        print('[INTENT] Error getting active blocks:', e)
        return jsonify({'error': 'Failed to fetch active blocks'}), 500


@intent_bp.route('/', methods=['POST'])
@verify_token
# @intent_limiter()
@maintenance_gate
@identity_guard
def create_intent_block():
    try:
        data = request.get_json(silent=True) or {}
        design_id = data.get('design_id')
        
        if not design_id:
            return jsonify({'error': 'design_id required'}), 400

        user_id = g.user.get('id')
        result = create_block(user_id, int(design_id))

        return jsonify({
            'message': 'Design blocked successfully',
            'data': result
        }), 201
    except ValueError as ve:
        print('[INTENT] Block failed (Validation):', ve)
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print('[INTENT] Block failed:', e)
        return jsonify({'error': 'Failed to block design'}), 500

@intent_bp.route('/<int:user_id>', methods=['GET'])
@verify_token
def get_user_wallet(user_id):
    try:
        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            if not wallet:
                return jsonify({'error': 'Wallet not found'}), 404

            transactions = db.execute('''
                SELECT * FROM wallet_transactions 
                WHERE wallet_id = ? 
                ORDER BY created_at DESC LIMIT 10
            ''', (wallet['wallet_id'],)).fetchall()

            return jsonify({
                'balance': wallet['balance'],
                'last_updated': wallet['last_updated'],
                'recent_activity': [dict(t) for t in transactions]
            })
    except Exception as e:
        print('[INTENT] Error getting wallet:', e)
        return jsonify({'error': 'Failed to fetch wallet info'}), 500

@intent_bp.route('/ledger/<int:user_id>', methods=['GET'])
@verify_token
def get_user_ledger(user_id):
    try:
        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            if not wallet:
                return jsonify({'error': 'Wallet not found'}), 404

            transactions = db.execute('''
                SELECT * FROM wallet_transactions 
                WHERE wallet_id = ? 
                ORDER BY created_at DESC
            ''', (wallet['wallet_id'],)).fetchall()

            return jsonify([dict(t) for t in transactions])
    except Exception as e:
        print('[INTENT] Error getting ledger:', e)
        return jsonify({'error': 'Failed to fetch ledger'}), 500

@intent_bp.route('/status/<int:design_id>', methods=['GET'])
@verify_token
def get_block_status(design_id):
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            block = db.execute('''
                SELECT * FROM blocks 
                WHERE design_id = ? AND status = 'active'
            ''', (design_id,)).fetchone()

            if not block:
                return jsonify({'status': 'available'})

            if block['user_id'] == user_id:
                return jsonify({
                    'status': 'blocked_by_me',
                    'block_id': block['block_id'],
                    'expiry_time': block['expiry_time']
                })

            return jsonify({'status': 'blocked_by_other'})
    except Exception as e:
        print('[INTENT] Error getting block status:', e)
        return jsonify({'error': 'Failed to fetch block status'}), 500
