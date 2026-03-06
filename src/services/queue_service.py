import json
from datetime import datetime
from src.config.db import get_db

class QueueService:
    def publish(self, event, payload, db_conn=None):
        try:
            if db_conn:
                self._insert(db_conn, event, payload)
            else:
                with get_db() as db:
                    self._insert(db, event, payload)
            print(f"[QUEUE] Event Published: {event}")
        except Exception as e:
            print(f"[QUEUE] Failed to publish event {event}: {str(e)}")
            
    def _insert(self, db, event, payload):
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('''
            INSERT INTO notification_queue (event_type, payload, status, next_attempt_at)
            VALUES (?, ?, ?, ?)
        ''', (event, json.dumps(payload), 'pending', now))

queue_service = QueueService()
