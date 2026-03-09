import sqlite3
import os

# Check platform.sqlite
if os.path.exists('platform.sqlite'):
    print("platform.sqlite exists")
    conn = sqlite3.connect('platform.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  Tables: {[t[0] for t in tables]}")
    
    if tables:
        cursor.execute('SELECT COUNT(*) FROM designs')
        print(f"  Designs count: {cursor.fetchone()[0]}")
        cursor.execute('SELECT COUNT(*) FROM design_media')
        print(f"  Design media count: {cursor.fetchone()[0]}")
    conn.close()
else:
    print("platform.sqlite does NOT exist")

# Check src/database/dev.sqlite3
if os.path.exists('src/database/dev.sqlite3'):
    print("\nsrc/database/dev.sqlite3 exists")
    conn = sqlite3.connect('src/database/dev.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  Tables: {[t[0] for t in tables]}")
    
    if tables:
        cursor.execute('SELECT COUNT(*) FROM designs')
        print(f"  Designs count: {cursor.fetchone()[0]}")
        cursor.execute('SELECT COUNT(*) FROM design_media')
        print(f"  Design media count: {cursor.fetchone()[0]}")
    conn.close()
else:
    print("\nsrc/database/dev.sqlite3 does NOT exist")
