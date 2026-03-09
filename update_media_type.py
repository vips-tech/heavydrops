import sqlite3

conn = sqlite3.connect('src/database/dev.sqlite3')
cursor = conn.cursor()

# Update primary images to have type 'master'
cursor.execute("UPDATE design_media SET type = 'master' WHERE is_primary = 1")
conn.commit()
print(f'Updated {cursor.rowcount} records to type=master')

# Verify
cursor.execute('SELECT design_id, url, type, is_primary FROM design_media')
rows = cursor.fetchall()
print('\nDesign media:')
for row in rows:
    print(f'  Design {row[0]}: {row[1]} (type={row[2]}, primary={row[3]})')

conn.close()
