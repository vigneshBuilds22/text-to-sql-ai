import sqlite3
connection =sqlite3.connect("data/sales.db")
cursor =connection.cursor()
cursor.execute("SELECT * FROM customers")
customers = cursor.fetchall()
print("customers:",customers)
for customer in customers:
    print("customer:",customer)
connection.close()