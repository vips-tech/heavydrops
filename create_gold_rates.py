import sqlite3
from datetime import datetime

conn = sqlite3.connect('src/database/dev.sqlite3')
cursor = conn.cursor()

# Create gold_rates table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gold_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purity VARCHAR(10) NOT NULL,
        rate_per_gram DECIMAL(14, 2) NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Insert default rates
cursor.execute('DELETE FROM gold_rates')  # Clear any existing data
cursor.executemany(
    'INSERT INTO gold_rates (purity, rate_per_gram) VALUES (?, ?)',
    [
        ('22K', 6200.00),
        ('24K', 6800.00),
        ('18K', 5400.00)
    ]
)

conn.commit()
print('Created gold_rates table and inserted default rates')

# Verify
cursor.execute('SELECT * FROM gold_rates')
rates = cursor.fetchall()
print('\nGold rates:')
for rate in rates:
    print(f'  {rate}')

conn.close()
