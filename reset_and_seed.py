"""
Reset Demo Data and Seed 50+ Jewelry Designs
Clears existing demo designs and creates fresh high-quality data
"""

import sqlite3
import sys

def reset_and_seed():
    db_path = "platform.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗑️  Clearing existing demo data...")
        
        # Delete demo design media first (foreign key constraint)
        cursor.execute("DELETE FROM design_media WHERE is_demo = 1 OR is_demo = 'true'")
        deleted_media = cursor.rowcount
        print(f"   Deleted {deleted_media} demo media entries")
        
        # Delete demo designs
        cursor.execute("DELETE FROM designs WHERE is_demo = 1 OR is_demo = 'true'")
        deleted_designs = cursor.rowcount
        print(f"   Deleted {deleted_designs} demo designs")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Demo data cleared successfully!")
        print("\n🌱 Now seeding 60 new jewelry designs...")
        print("=" * 50)
        
        # Import and run the seed function
        from seed_50_designs import seed_50_designs
        seed_50_designs()
        
        print("\n" + "=" * 50)
        print("✅ All done! Your jewelry catalog is ready!")
        print("\n📋 Summary:")
        print("   - 60 high-quality jewelry designs")
        print("   - 4 cards per row on desktop")
        print("   - 15 rows total")
        print("   - Unique images for each design")
        print("   - Proper product names and descriptions")
        print("\n🚀 Start your server to see the results:")
        print("   python app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_and_seed()
