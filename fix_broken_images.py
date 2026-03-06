import sqlite3
import requests
import os

DB_PATH = 'd:\\HeavyDrops_Platform_v1.0\\platform.sqlite'

def find_broken_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT media_id, design_id, uri FROM design_media WHERE status='approved'")
    media = cursor.fetchall()
    
    broken_media_ids = []
    print(f"Checking {len(media)} images...")
    
    for row in media:
        media_id, design_id, uri = row
        try:
            if uri.startswith('/'):
                file_path = f"d:\\HeavyDrops_Platform_v1.0\\public{uri.replace('/', '\\\\')}"
                if not os.path.exists(file_path):
                    broken_media_ids.append(str(media_id))
            elif uri.startswith('http'):
                try:
                    response = requests.head(uri, timeout=2, verify=False)
                    if response.status_code >= 400:
                        response = requests.get(uri, timeout=2, verify=False)
                        if response.status_code >= 400:
                            broken_media_ids.append(str(media_id))
                except requests.exceptions.RequestException:
                    broken_media_ids.append(str(media_id))
        except Exception:
            broken_media_ids.append(str(media_id))
            
    print(f"Found {len(broken_media_ids)} broken media rows.")
    if len(broken_media_ids) > 0:
        ids = ','.join(broken_media_ids)
        cursor.execute(f"DELETE FROM design_media WHERE media_id IN ({ids})")
        
        cursor.execute('SELECT design_id FROM designs d WHERE NOT EXISTS (SELECT 1 FROM design_media dm WHERE dm.design_id = d.design_id)')
        orphan_designs = cursor.fetchall()
        if orphan_designs:
            orphan_ids = ','.join([str(d[0]) for d in orphan_designs])
            cursor.execute(f"DELETE FROM likes WHERE design_id IN ({orphan_ids})")
            cursor.execute(f"DELETE FROM designs WHERE design_id IN ({orphan_ids})")
            print(f"Deleted {len(orphan_designs)} orphan designs without any media.")
        conn.commit()
    conn.close()

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    find_broken_images()
