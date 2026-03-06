from datetime import datetime
import time
from src.config.db import get_db
from src.services.queue_service import queue_service

def penalize_no_show(user_id, block_id, db_conn=None):
    def execute(db):
        print(f"[DEBUG] penalizeNoShow for User #{user_id}, Block #{block_id}")
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        if not user:
            print(f"[DEBUG] User #{user_id} not found in trust penalty")
            return

        new_strike_count = (user.get('strike_count') or 0) + 1
        new_status = 'restricted' if new_strike_count >= 3 else 'active'
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        db.execute('''
            UPDATE users SET strike_count = ?, status = ?, updated_at = ?
            WHERE user_id = ?
        ''', (new_strike_count, new_status, now, user_id))

        wallet = db.execute('SELECT * FROM wallets WHERE user_id = ?', (user_id,)).fetchone()
        if wallet and wallet['balance'] >= 100:
            penalty_ref = f"PEN-{block_id}-{str(int(time.time()*1000))[-6:]}"
            db.execute('UPDATE wallets SET balance = balance - 100 WHERE user_id = ?', (user_id,))
            db.execute('''
                INSERT INTO wallet_transactions (wallet_id, amount, type, source_type, description, reference_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (wallet['wallet_id'], -100, 'debit', 'penalty', f"No-show penalty for block #{block_id}", penalty_ref))

        db.execute('''
            INSERT INTO violations (entity_type, entity_id, type, level, reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'user', user_id, 'no_show', 
            'high' if new_strike_count >= 3 else 'medium', 
            f"Appointment no-show. Total strikes: {new_strike_count}"
        ))

        queue_service.publish('appointment.no_show', {
            'user_id': user_id,
            'block_id': block_id,
            'strikes': new_strike_count
        }, db)

        print(f"[TRUST] No-show penalty applied to User #{user_id}. Strikes: {new_strike_count}")

    if db_conn:
        return execute(db_conn)
    else:
        with get_db() as db:
            return execute(db)

def update_seller_trust(seller_id, delta, reason):
    with get_db() as db:
        db.execute('UPDATE sellers SET trust_score = trust_score + ? WHERE seller_id = ?', (delta, seller_id))
        
        v_type = 'score_deduction' if delta < 0 else 'score_increase'
        db.execute('''
            INSERT INTO violations (entity_type, entity_id, type, reason)
            VALUES (?, ?, ?, ?)
        ''', ('seller', seller_id, v_type, reason))
