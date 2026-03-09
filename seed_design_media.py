import sqlite3

conn = sqlite3.connect('src/database/dev.sqlite3')
cursor = conn.cursor()

# Add media for the existing designs
media_data = [
    (4, '/assets/goldbanglescover.jpg', 'image', 1),
    (5, '/assets/OIP (1).jpg', 'image', 1),
    (6, '/assets/goldbanglescover.jpg', 'image', 1)
]

cursor.executemany(
    'INSERT INTO design_media (design_id, url, type, is_primary) VALUES (?, ?, ?, ?)',
    media_data
)

conn.commit()
print(f'Added {cursor.rowcount} media records for designs')

# Verify
cursor.execute('SELECT design_id, url FROM design_media')
rows = cursor.fetchall()
print('\nCurrent design_media:')
for row in rows:
    print(f'  Design {row[0]}: {row[1]}')

conn.close()
