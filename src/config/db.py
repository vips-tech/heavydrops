import sqlite3
import os
from contextlib import contextmanager

# Base directory is one level up from this file's directory (src -> HeavyDrops_Platform_v1.0)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'platform.sqlite')

def dict_factory(cursor, row):
    """
    Row factory to return dicts instead of tuples from sqlite3
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    """
    Returns a new SQLite database connection with WAL mode enabled and dict factory setup.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    # Enable WAL mode for better concurrency, matching the previous Knex setup
    conn.execute('PRAGMA journal_mode = WAL')
    # Enable foreign keys
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

@contextmanager
def get_db():
    """
    Context manager for database connections.
    Usage:
        with get_db() as db:
            db.execute("SELECT * FROM users")
    """
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
