import sqlite3
import random

def seed_more():
    db_path = "platform.sqlite"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get existing sellers
    sellers = cursor.execute("SELECT seller_id FROM sellers WHERE is_demo = 1 or is_demo = 'true'").fetchall()
    if not sellers:
        # Fallback if no demo sellers, just get any sellers
        sellers = cursor.execute("SELECT seller_id FROM sellers").fetchall()
    
    seller_ids = [s['seller_id'] for s in sellers]
    if not seller_ids:
        print("No sellers found to assign designs to!")
        return

    necklace_images = [
        'https://images.unsplash.com/photo-1599643477877-530eb83abc8e?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?auto=format&fit=crop&q=80&w=800'
    ]
    bangle_images = [
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1629224316170-f6bd44827d09?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?auto=format&fit=crop&q=80&w=800'
    ]

    new_designs = []
    
    # Generate 10 Necklaces
    for i in range(10):
        new_designs.append({
            'category': 'Necklace',
            'weight': round(15 + random.random() * 40, 2),
            'img': random.choice(necklace_images)
        })

    # Generate 10 Bangles
    for i in range(10):
        new_designs.append({
            'category': 'Bangles',
            'weight': round(5 + random.random() * 15, 2),
            'img': random.choice(bangle_images)
        })

    for d in new_designs:
        seller_id = random.choice(seller_ids)
        purity = random.choice(['18K', '22K'])
        weight = d['weight']
        rate = 6200
        mk_charge = 800 + random.randint(0, 500)
        
        cursor.execute('''
            INSERT INTO designs 
            (seller_id, category, purity, weight, gold_rate_snapshot, making_charge_snapshot, 
             media_quality_status, availability_status, view_count, like_count_snapshot, block_count_snapshot, is_demo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (seller_id, d['category'], purity, weight, rate, mk_charge, 'approved', 'available', 
              random.randint(50, 500), random.randint(5, 50), 0, True))
        
        design_id = cursor.lastrowid
        
        # Insert master and closeup media
        cursor.execute('''
            INSERT INTO design_media (design_id, uri, media_type, shot_type, status, is_demo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (design_id, d['img'], 'image', 'master', 'approved', True))
        
        cursor.execute('''
            INSERT INTO design_media (design_id, uri, media_type, shot_type, status, is_demo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (design_id, d['img'], 'image', 'closeup', 'approved', True))

    conn.commit()
    conn.close()
    print("Successfully seeded 10 more necklaces and 10 more bangles!")

if __name__ == "__main__":
    seed_more()
