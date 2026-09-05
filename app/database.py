import sqlite3

DATABASE_PATH = "data/sales.db"


def execute_query(sql):
    """
    Execute a read-only SQL query against the SQLite database.
    """
    connection = sqlite3.connect(
        f"file:{DATABASE_PATH}?mode=ro",
        uri=True
    )
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        return columns, rows

    finally:
        connection.close()