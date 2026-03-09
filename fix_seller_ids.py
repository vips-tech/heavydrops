import sqlite3

conn = sqlite3.connect('src/database/dev.sqlite3')
cursor = conn.cursor()

# Get the first seller ID
cursor.execute('SELECT seller_id FROM sellers LIMIT 1')
first_seller = cursor.fetchone()
seller_id = first_seller[0] if first_seller else 3

print(f"Updating designs to use seller_id: {seller_id}")

# Update all designs to have a valid seller_id
cursor.execute('UPDATE designs SET seller_id = ?', (seller_id,))

conn.commit()
print(f"Updated {cursor.rowcount} designs")

# Verify
cursor.execute('SELECT design_id, seller_id FROM designs')
designs = cursor.fetchall()
print('\nUpdated designs:')
for design in designs:
    print(f'  Design {design[0]}: seller_id = {design[1]}')

conn.close()
