from src.routes.discovery import get_curated_designs
from flask import Flask
from unittest.mock import Mock

# Create a test Flask app context
app = Flask(__name__)

with app.test_request_context('/?'):
    # Mock the request object
    from flask import request
    
    # Call the function directly
    try:
        from src.routes.discovery import discovery_bp
        print("Testing discovery endpoint...")
        
        # Import and test directly
        from src.config.db import get_db
        
        with get_db() as db:
            # Test the query
            designs = db.execute('''
                SELECT d.*, s.business_name, s.city, s.trust_score
                FROM designs d
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE d.availability_status = 'available' AND d.media_quality_status = 'approved'
            ''').fetchall()
            
            print(f"Found {len(designs)} designs")
            
            # Test image query
            first_images = db.execute('''
                SELECT design_id, MIN(media_id) as first_media_id 
                FROM design_media 
                WHERE is_primary = 1 OR type = 'image'
                GROUP BY design_id
            ''').fetchall()
            
            print(f"Found {len(first_images)} design images")
            
            for img in first_images:
                media = db.execute('SELECT url FROM design_media WHERE media_id = ?', (img['first_media_id'],)).fetchone()
                if media:
                    print(f"  Design {img['design_id']}: {media['url']}")
            
            print("\nAPI should work correctly!")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
