"""
This script will create or reset the ads table in the database to its initial
state, with 3 sample ads.
"""

import sqlite3

conn = sqlite3.connect('bsrh.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS ads')
cursor.execute('''
    CREATE TABLE ads (
        id INTEGER PRIMARY KEY,
        category TEXT,
        title TEXT)
''')
cursor.execute('''
    INSERT INTO ads (category, title) VALUES
    ('Motors', 'Yamaha FZ6-N'),
    ('Electronics', 'Google Pixel 3')
''')
conn.commit()
conn.close()
