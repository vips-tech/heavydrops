"""Direct test of the discovery endpoint logic"""
import sys
import traceback

try:
    from src.config.db import get_db
    
    print("Testing database connection and query...")
    
    with get_db() as db:
        # Test gold rates
        rates = db.execute('SELECT * FROM gold_rates ORDER BY updated_at DESC').fetchall()
        print(f"Gold rates: {len(rates)} found")
        
        rate_map = {'22K': 6200, '24K': 6800}
        for r in rates:
            if r['purity'] not in rate_map or r == rates[0]:
                rate_map[r['purity']] = float(r['rate_per_gram'])
        print(f"Rate map: {rate_map}")
        
        # Test images
        first_images = db.execute('''
            SELECT design_id, MIN(media_id) as first_media_id 
            FROM design_media 
            WHERE is_primary = 1 OR type = 'image'
            GROUP BY design_id
        ''').fetchall()
        print(f"First images: {len(first_images)} found")
        
        image_map = {}
        for img in first_images:
            media = db.execute('SELECT url FROM design_media WHERE media_id = ?', (img['first_media_id'],)).fetchone()
            if media:
                image_map[img['design_id']] = media['url']
        print(f"Image map: {image_map}")
        
        # Test likes
        like_counts = db.execute('SELECT design_id, COUNT(*) as likes_count FROM likes GROUP BY design_id').fetchall()
        like_map = {l['design_id']: l['likes_count'] for l in like_counts}
        print(f"Like map: {like_map}")
        
        # Test main query
        query = '''
            SELECT d.*, s.business_name, s.city, s.trust_score
            FROM designs d
            JOIN sellers s ON d.seller_id = s.seller_id
            WHERE d.availability_status = 'available' AND d.media_quality_status = 'approved'
        '''
        designs = db.execute(query).fetchall()
        print(f"\nDesigns found: {len(designs)}")
        
        # Process first design
        if designs:
            design = designs[0]
            print(f"\nFirst design: {design['design_id']}")
            print(f"  Category: {design['category']}")
            print(f"  Purity: {design['purity']}")
            print(f"  Weight: {design['weight']}")
            print(f"  Seller: {design['business_name']}")
            
            current_rate = rate_map.get(design['purity'], rate_map.get('22K', 6200))
            gold_value = design['weight'] * current_rate
            subtotal = gold_value + design['making_charge_snapshot']
            gst = subtotal * 0.03
            total_price = subtotal + gst
            
            print(f"  Gold rate: {current_rate}")
            print(f"  Gold value: {gold_value}")
            print(f"  Total price: {total_price}")
            print(f"  Image: {image_map.get(design['design_id'])}")
            
        print("\n✓ All queries work correctly!")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    traceback.print_exc()
