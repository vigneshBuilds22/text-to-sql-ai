import sqlite3
connection = sqlite3.connect("data/sales.db")
cursor =connection.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")
customers = [(1,'Arun','chennai'),
             (2,'Ravi','bangalore'),
             (3,'kumar','delhi'),
             (4,'Ramesh','mumbai'),
             (5,'Suresh','kolkata')]
products = [(1,'Laptop','Electronics',50000),
            (2,'mobile','Electronics',20000),
            (3,'TV','Electronics',30000),
            (4,'Refrigerator','Electronics',40000),
            (5,'Washing Machine','Electronics',25000)]
orders = [(1,1,1,4,'2023-01-01'),
          (2,2,2,2,'2023-01-02'),
          (3,3,3,1,'2023-01-03'),
          (4,4,4,3,'2023-01-04'),
          (5,5,5,2,'2023-01-05')]
cursor.executemany("INSERT INTO customers VALUES (?,?,?)", customers)
cursor.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?)",orders)
connection.commit()
connection.close()
print("DB created successfully")