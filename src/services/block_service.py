import os
from datetime import datetime, timedelta
from src.config.db import get_db
from src.services.queue_service import queue_service

def create_block(user_id, design_id, db_conn=None, reference_id=None):
    def execute(db):
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        strikes = user.get('strike_count', 0) if user else 0
        limit_env = os.environ.get('ACTIVE_BLOCK_LIMIT', '2')
        max_active_blocks = 1 if strikes >= 2 else int(limit_env)

        active_blocks = db.execute(
            "SELECT COUNT(*) as count FROM blocks WHERE user_id = ? AND status = 'active'", 
            (user_id,)
        ).fetchone()

        if active_blocks and active_blocks['count'] >= max_active_blocks:
            raise ValueError(f"Active block limit reached ({max_active_blocks}). Strike penalty active: {strikes >= 2}")

        design = db.execute(
            "SELECT * FROM designs WHERE design_id = ? AND availability_status = 'available'",
            (design_id,)
        ).fetchone()

        if not design:
            raise ValueError('Design is currently unavailable or already blocked.')

        wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
        block_fee = int(os.environ.get('BLOCK_FEE_MIN', '100'))

        if not wallet or wallet['balance'] < block_fee:
            raise ValueError(f"Insufficient wallet balance. Minimum block fee required: ₹{block_fee}")

        expiry_hours = int(os.environ.get('BLOCK_EXPIRY_HOURS', '48'))
        expiry_time = (datetime.utcnow() + timedelta(hours=expiry_hours)).strftime('%Y-%m-%d %H:%M:%S')

        design_price = (design['weight'] * design['gold_rate_snapshot']) + design['making_charge_snapshot']

        # 5. Execute Block Creation
        cursor = db.execute('''
            INSERT INTO blocks (user_id, design_id, price_snapshot, status, expiry_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, design_id, design_price, 'active', expiry_time))
        block_id = cursor.lastrowid

        # 6. Lock Design
        db.execute("UPDATE designs SET availability_status = 'blocked' WHERE design_id = ?", (design_id,))

        # 7. Ledger Entry (Debit)
        db.execute('''
            INSERT INTO wallet_transactions (wallet_id, amount, type, source_type, description, reference_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (wallet['wallet_id'], -block_fee, 'debit', 'block_payment', f"Commitment fee for design #{design_id}", reference_id))

        # 8. Update Wallet Balance
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('''
            UPDATE wallets SET balance = balance - ?, last_updated = ? WHERE user_id = ?
        ''', (block_fee, now, user_id))

        # 9. Emit Notification Event
        queue_service.publish('block.created', {
            'user_id': user_id,
            'design_id': design_id,
            'expiry_time': expiry_time
        }, db)

        return {
            'block_id': block_id,
            'expiry_time': expiry_time,
            'locked_price': design_price
        }

    if db_conn:
        return execute(db_conn)
    else:
        with get_db() as db:
            return execute(db)

def expire_block(block_id):
    with get_db() as db:
        block = db.execute("SELECT * FROM blocks WHERE block_id = ? AND status = 'active'", (block_id,)).fetchone()
        if not block:
            return

        db.execute("UPDATE designs SET availability_status = 'available' WHERE design_id = ?", (block['design_id'],))
        db.execute("UPDATE blocks SET status = 'expired' WHERE block_id = ?", (block_id,))
        db.execute("UPDATE appointments SET status = 'cancelled' WHERE block_id = ? AND status = 'requested'", (block_id,))

        queue_service.publish('block.expired', {
            'user_id': block['user_id'],
            'design_id': block['design_id']
        }, db)
        
        # Balance is NOT returned on expiry.
