import os
import random
import time
from flask import Blueprint, jsonify, request, g
from src.config.db import get_db
from src.services.block_service import create_block
from src.middleware.auth import verify_token
from src.middleware.identity_guard import identity_guard

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/initiate', methods=['POST'])
@verify_token
@identity_guard
def initiate_payment():
    try:
        data = request.get_json(silent=True) or {}
        design_id = data.get('design_id')
        user_id = g.user.get('id')
        
        if not design_id:
            return jsonify({'error': 'design_id required'}), 400

        with get_db() as db:
            active_blocks = db.execute('''
                SELECT COUNT(*) as count FROM blocks 
                WHERE user_id = ? AND status = 'active'
            ''', (user_id,)).fetchone()
            
            if active_blocks and int(active_blocks['count']) >= 2:
                return jsonify({'error': 'Max 2 active intent blocks allowed.'}), 400

        transaction_id = f"TXN-{str(int(time.time()*1000))[-9:].upper()}"
        block_fee = int(os.environ.get('BLOCK_FEE_MIN', '500'))

        return jsonify({
            'message': 'Payment initiated',
            'transaction_id': transaction_id,
            'block_fee': block_fee,
            'gateway_sim_url': f"/pay-sim.html?design_id={design_id}"
        })
    except Exception as e:
        print('[PAYMENT] Initiation failed:', e)
        return jsonify({'error': 'Payment initiation failed'}), 500

@payment_bp.route('/callback', methods=['POST'])
@verify_token
@identity_guard
def handle_success():
    print('[DEBUG] Entering handleSuccess')
    try:
        data = request.get_json(silent=True) or {}
        design_id = data.get('design_id')
        status = data.get('status')
        user_id = g.user.get('id')
        
        print(f"[DEBUG] handleSuccess for User #{user_id}, Design #{design_id}, Status: {status}")

        if status != 'success':
            return jsonify({'error': 'Payment status not successful'}), 400

        block_fee = int(os.environ.get('BLOCK_FEE_MIN', '500'))
        cycle_ref = f"CYC-{str(int(time.time()*1000))[-9:].upper()}"

        with get_db() as db:
            wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
            if not wallet:
                return jsonify({'error': 'Wallet not initialized for user'}), 400

            # 1. Credit Wallet
            new_balance = wallet['balance'] + block_fee
            from datetime import datetime
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            db.execute('UPDATE wallets SET balance = ?, last_updated = ? WHERE user_id = ?', 
                      (new_balance, now, user_id))

            db.execute('''
                INSERT INTO wallet_transactions (wallet_id, amount, type, source_type, description, reference_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (wallet['wallet_id'], block_fee, 'credit', 'payment_gateway', 
                 f"Top-up for design block #{design_id}", cycle_ref))

            # 2. Trigger block creation
            block = create_block(user_id, design_id, db, cycle_ref)
            
        print(f"[PAYMENT] Success: Design #{design_id} blocked for User #{user_id}")

        return jsonify({
            'status': 'success',
            'message': 'Payment verified and Block created.',
            'block_id': block['block_id'],
            'expiry_time': block['expiry_time']
        })

    except Exception as e:
        print('[PAYMENT] Processing failed:', e)
        return jsonify({'error': f"Payment processing failed: {str(e)}"}), 400
