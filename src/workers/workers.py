import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from src.config.db import get_db
from src.services.block_service import expire_block
from src.services.queue_service import queue_service

# Expiry Worker Functions
def run_expiry_job():
    print('[WORKER] Starting Block Expiry scan...')
    try:
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        with get_db() as db:
            expired_blocks = db.execute('''
                SELECT * FROM blocks 
                WHERE status = 'active' AND expiry_time <= ? 
                LIMIT 50
            ''', (now,)).fetchall()

            warning_time = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            nearing_expiry = db.execute('''
                SELECT * FROM blocks 
                WHERE status = 'active' AND expiry_time <= ? AND expiry_time > ?
            ''', (warning_time, now)).fetchall()

            for block in nearing_expiry:
                queue_service.publish('block.expiry_warning', {
                    'user_id': block['user_id'],
                    'design_id': block['design_id']
                }, db)

            print(f"[WORKER] Found {len(expired_blocks)} blocks to expire.")

            for block in expired_blocks:
                expire_block(block['block_id'])
                print(f"[WORKER] Expired Block #{block['block_id']} (Design #{block['design_id']})")

            if expired_blocks:
                print(f"[WORKER] Successfully flushed {len(expired_blocks)} design blocks.")
                
    except Exception as e:
        print('[WORKER] Block expiry job failed:', e)

def audit_wallet_activity():
    print('[WORKER] Starting Wallet Activity Audit...')
    try:
        stale_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        with get_db() as db:
            stale_wallets = db.execute('SELECT * FROM wallets WHERE last_updated < ?', (stale_date,)).fetchall()
            print(f"[WORKER] Audited {len(stale_wallets)} inactive wallets.")
    except Exception as e:
        print('[WORKER] Wallet audit failed:', e)

def process_appointment_reminders():
    print('[WORKER] Checking for upcoming appointment reminders...')
    try:
        soon = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        with get_db() as db:
            reminders = db.execute('''
                SELECT * FROM appointments 
                WHERE status = 'confirmed' AND appointment_time <= ?
            ''', (soon,)).fetchall()

            for appt in reminders:
                print(f"[WORKER] [REMINDER] Alerting User #{appt['user_id']} for appointment #{appt['appointment_id']}")
                queue_service.publish('appointment.reminder', {
                    'user_id': appt['user_id'],
                    'design_id': appt['design_id'],
                    'time': appt['appointment_time']
                }, db)
    except Exception as e:
        print('[WORKER] Reminder job failed:', e)

def process_abuse_detection():
    print('[WORKER] Scanning for platform abuse signals...')
    try:
        with get_db() as db:
            suspicious_users = db.execute('''
                SELECT * FROM users 
                WHERE strike_count >= 3 AND role != 'suspended'
            ''').fetchall()

            for user in suspicious_users:
                print(f"[WORKER] [ABUSE] Automated suspension for User #{user['user_id']} due to strike count ({user['strike_count']})")
                
                now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                db.execute('UPDATE users SET role = ?, updated_at = ? WHERE user_id = ?', 
                          ('suspended', now, user['user_id']))
                
                db.execute('''
                    INSERT INTO violations (entity_type, entity_id, type, reason, level)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('buyer', user['user_id'], 'abuse_automated', 'Automated suspension: Strike count limit (3) exceeded.', 'critical'))
                
                active_blocks = db.execute('SELECT * FROM blocks WHERE user_id = ? AND status = ?', 
                                          (user['user_id'], 'active')).fetchall()
                for block in active_blocks:
                    expire_block(block['block_id'])
                    
    except Exception as e:
        print('[WORKER] Abuse detection failed:', e)

# Notification Worker
def process_notification_queue():
    try:
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with get_db() as db:
            jobs = db.execute('''
                SELECT * FROM notification_queue 
                WHERE (status = 'pending' OR (status = 'failed' AND attempts < 3))
                AND next_attempt_at <= ?
                LIMIT 10
            ''', (now,)).fetchall()

            for job in jobs:
                db.execute('UPDATE notification_queue SET status = ? WHERE job_id = ?', ('processing', job['job_id']))
                # Note: Skipping actual SMS/Email sending logic simulation as messagingService is complex.
                # In MVP, we mark as sent.
                
                try:
                    import json
                    payload = json.loads(job['payload'])
                    user_id = payload.get('user_id')
                    
                    # Channels mock
                    types_mapping = {
                        'block.created': 'sms', 'appointment.booked': 'sms', 'appointment.no_show': 'sms',
                        'block.expiry_warning': 'email', 'appointment.reminder': 'email', 'seller.violation': 'email'
                    }
                    channel = types_mapping.get(job['event_type'], 'in_app')

                    db.execute('''
                        INSERT INTO notifications (user_id, type, channel, status, payload)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (user_id, job['event_type'], channel, 'sent', job['payload']))

                    db.execute('UPDATE notification_queue SET status = ? WHERE job_id = ?', ('completed', job['job_id']))
                except Exception as ex:
                    print(f"[NOTIFIER] Job #{job['job_id']} failed: {ex}")
                    next_attempt = (datetime.utcnow() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
                    db.execute('''
                        UPDATE notification_queue 
                        SET status = 'failed', attempts = attempts + 1, next_attempt_at = ? 
                        WHERE job_id = ?
                    ''', (next_attempt, job['job_id']))

    except Exception as e:
        print('[NOTIFIER] Queue processing error:', e)

def start_workers():
    print('[SYSTEM] Background Workers Initialized using APScheduler.')
    scheduler = BackgroundScheduler()
    
    # Expiry Worker (every 10 minutes)
    scheduler.add_job(func=run_expiry_job, trigger="interval", minutes=10)
    
    # Wallet Audit (every 24 hours)
    scheduler.add_job(func=audit_wallet_activity, trigger="interval", hours=24)
    
    # Reminders (every 15 minutes)
    scheduler.add_job(func=process_appointment_reminders, trigger="interval", minutes=15)
    
    # Abuse Detection (every 6 hours)
    scheduler.add_job(func=process_abuse_detection, trigger="interval", hours=6)
    
    # Notification Worker (every 30 seconds)
    scheduler.add_job(func=process_notification_queue, trigger="interval", seconds=30)
    
    scheduler.start()
    
    # Fire initial jobs
    try:
        run_expiry_job()
        audit_wallet_activity()
        process_appointment_reminders()
        process_abuse_detection()
    except Exception as e:
        print("Error in initial worker firing", e)
