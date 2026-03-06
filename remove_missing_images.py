import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'platform.sqlite')

def remove_designs_without_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check how many designs have no images
    cursor.execute('''
        SELECT d.design_id, d.category 
        FROM designs d
        LEFT JOIN design_media dm ON d.design_id = dm.design_id
        WHERE dm.media_id IS NULL
    ''')
    
    no_image_designs = cursor.fetchall()
    print(f"Found {len(no_image_designs)} designs without images.")
    
    if len(no_image_designs) > 0:
        design_ids = [str(d[0]) for d in no_image_designs]
        ids_str = ','.join(design_ids)
        
        # Delete likes for these designs first (foreign key constraints)
        cursor.execute(f"DELETE FROM likes WHERE design_id IN ({ids_str})")
        print(f"Deleted related likes.")
        
        # Then delete the designs
        cursor.execute(f"DELETE FROM designs WHERE design_id IN ({ids_str})")
        print(f"Deleted {len(no_image_designs)} designs without images.")
        
        conn.commit()
    
    conn.close()

if __name__ == '__main__':
    remove_designs_without_images()
