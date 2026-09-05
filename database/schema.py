import sqlite3

connection = sqlite3.connect("data/sales.db")
cursor = connection.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

for table in tables:
    table_name = table[0]

    print(f"\nTABLE: {table_name}")

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        print(f"  - {column[1]} ({column[2]})")

connection.close()