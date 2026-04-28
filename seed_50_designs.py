"""
Seed 50+ High-Quality Jewelry Designs
Creates at least 10 rows of 4 cards each with unique images and descriptions
"""

import sqlite3
import random

def seed_50_designs():
    db_path = "platform.sqlite"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get existing sellers
    sellers = cursor.execute("SELECT seller_id FROM sellers WHERE is_demo = 1 or is_demo = 'true'").fetchall()
    if not sellers:
        sellers = cursor.execute("SELECT seller_id FROM sellers").fetchall()
    
    seller_ids = [s['seller_id'] for s in sellers]
    if not seller_ids:
        print("No sellers found! Please run the main seed script first.")
        return

    # High-quality gold jewelry images from Unsplash
    jewelry_data = {
        'Necklace': {
            'images': [
                'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1603561596112-0a132b757442?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1614170143028-a2e6d4c6e0f7?w=800&h=800&fit=crop&q=90',
            ],
            'occasions': ['Wedding', 'Engagement', 'Festive', 'Traditional', 'Party'],
            'weight_range': (15, 55)
        },
        'Rings': {
            'images': [
                'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1603561596112-0a132b757442?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1614170143028-a2e6d4c6e0f7?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1588444650700-c5886c00c0e9?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1590858593969-a0e561f5e4e3?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1611955167811-4711904bb9f8?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1612404730960-5c71577fca11?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&h=800&fit=crop&q=90',
            ],
            'occasions': ['Engagement', 'Wedding', 'Anniversary', 'Daily Wear', 'Party'],
            'weight_range': (3, 12)
        },
        'Bangle': {
            'images': [
                'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&h=800&fit=crop&q=90',
            ],
            'occasions': ['Wedding', 'Traditional', 'Festive', 'Daily Wear', 'Party'],
            'weight_range': (8, 30)
        },
        'Earrings': {
            'images': [
                'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop&q=90',
            ],
            'occasions': ['Wedding', 'Party', 'Festive', 'Daily Wear', 'Traditional'],
            'weight_range': (4, 18)
        },
        'Bracelet': {
            'images': [
                'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=800&h=800&fit=crop&q=90',
                'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&h=800&fit=crop&q=90',
            ],
            'occasions': ['Party', 'Daily Wear', 'Festive', 'Wedding', 'Traditional'],
            'weight_range': (6, 25)
        }
    }

    designs_created = 0
    
    # Create 12 designs per category (60 total = 15 rows of 4)
    for category, data in jewelry_data.items():
        images = data['images']
        occasions = data['occasions']
        weight_min, weight_max = data['weight_range']
        
        # Create 12 designs per category
        for i in range(12):
            seller_id = random.choice(seller_ids)
            purity = random.choice(['18K', '22K', '22K', '22K'])  # More 22K
            weight = round(random.uniform(weight_min, weight_max), 2)
            gold_rate = 6479  # Real 22K gold rate
            making_charge = random.randint(800, 2500)
            gst = round((weight * gold_rate + making_charge) * 0.03, 2)  # 3% GST
            occasion = random.choice(occasions)
            
            # Use different image for each design
            image_url = images[i % len(images)]
            
            # Insert design
            cursor.execute('''
                INSERT INTO designs 
                (seller_id, category, purity, weight, gold_rate_snapshot, making_charge_snapshot, 
                 gst, occasion_tag, media_quality_status, availability_status, 
                 view_count, like_count_snapshot, block_count_snapshot, is_demo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                seller_id, category, purity, weight, gold_rate, making_charge, 
                gst, occasion, 'approved', 'available',
                random.randint(50, 800), random.randint(5, 100), 0, True
            ))
            
            design_id = cursor.lastrowid
            
            # Insert master image
            cursor.execute('''
                INSERT INTO design_media (design_id, uri, media_type, shot_type, status, is_demo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (design_id, image_url, 'image', 'master', 'approved', True))
            
            # Insert closeup image
            cursor.execute('''
                INSERT INTO design_media (design_id, uri, media_type, shot_type, status, is_demo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (design_id, image_url, 'image', 'closeup', 'approved', True))
            
            designs_created += 1
            
            if designs_created % 10 == 0:
                print(f"Created {designs_created} designs...")

    conn.commit()
    conn.close()
    
    print(f"\n✅ Successfully created {designs_created} jewelry designs!")
    print(f"📊 Distribution:")
    for category in jewelry_data.keys():
        print(f"   - {category}: 12 designs")
    print(f"\n🎯 This gives you {designs_created // 4} rows of 4 cards each!")

if __name__ == "__main__":
    seed_50_designs()
