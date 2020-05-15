"""
This script will reset the bsrh database to its initial state.
"""

import sqlite3

conn = sqlite3.connect('bsrh.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS ad')
cursor.execute('DROP TABLE IF EXISTS user')
cursor.execute('DROP TABLE IF EXISTS followers')

conn.commit()
conn.close()
