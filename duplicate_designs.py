import sqlite3

conn = sqlite3.connect('src/database/dev.sqlite3')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get existing designs
cursor.execute('SELECT * FROM designs')
existing_designs = cursor.fetchall()

print(f"Found {len(existing_designs)} existing designs")

# Get existing design media
cursor.execute('SELECT * FROM design_media')
existing_media = cursor.fetchall()

print(f"Found {len(existing_media)} existing media records")

# Duplicate designs 5 times
duplicates_to_create = 5
new_designs = []
new_media = []

for i in range(duplicates_to_create):
    for design in existing_designs:
        # Create new design with modified data
        cursor.execute('''
            INSERT INTO designs (
                seller_id, category, purity, weight, 
                gold_rate_snapshot, making_charge_snapshot,
                media_quality_status, availability_status,
                view_count, like_count_snapshot, block_count_snapshot
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            design['seller_id'],
            design['category'],
            design['purity'],
            design['weight'],
            design['gold_rate_snapshot'],
            design['making_charge_snapshot'],
            design['media_quality_status'],
            design['availability_status'],
            0,  # Reset view count
            0,  # Reset like count
            0   # Reset block count
        ))
        
        new_design_id = cursor.lastrowid
        new_designs.append(new_design_id)
        
        # Find and duplicate media for this design
        original_design_id = design['design_id']
        for media in existing_media:
            if media['design_id'] == original_design_id:
                cursor.execute('''
                    INSERT INTO design_media (design_id, url, type, is_primary)
                    VALUES (?, ?, ?, ?)
                ''', (
                    new_design_id,
                    media['url'],
                    media['type'],
                    media['is_primary']
                ))
                new_media.append(cursor.lastrowid)

conn.commit()

print(f"\nCreated {len(new_designs)} new designs")
print(f"Created {len(new_media)} new media records")

# Verify total count
cursor.execute('SELECT COUNT(*) FROM designs')
total_designs = cursor.fetchone()[0]
print(f"\nTotal designs in database: {total_designs}")

cursor.execute('SELECT COUNT(*) FROM design_media')
total_media = cursor.fetchone()[0]
print(f"Total media records: {total_media}")

conn.close()
