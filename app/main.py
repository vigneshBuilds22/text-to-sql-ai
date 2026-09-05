import sqlite3
from app.gemini_client import generate_Sql
from app.sql_validator import validate_sql
from app.database import execute_query
DATABASE_PATH = "data/sales.db"
def get_schema():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema_parts = []

    for (table_name,) in tables:

        schema_parts.append(f"TABLE: {table_name}")

        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns = cursor.fetchall()

        for column in columns:
            column_name = column[1]
            column_type = column[2]

            schema_parts.append(
                f" - {column_name} ({column_type})"
            )

    connection.close()

    return "\n".join(schema_parts)
def main():
    question = input("Enter your question about your data:")
    schema = get_schema()
    print("DATABASE SCHEMA:")
    print(schema)
    print("Generating sql query...")
    sql_query =generate_Sql(question,schema)
    print("Generated SQL query:")
    print(sql_query)
    print("validating sql query...")
    try:
        sql=validate_sql(sql_query)
        print("SQL Validation Successful")
    except ValueError as e:
        print(f"SQL Validation Failed: {e}")
        return
    print("Executing SQL query..")
    try:
        columns , rows = execute_query(sql)
        print("Query executed successfully. Results:")
        for row in rows:
            print(row)
    except EXCEPTION as e:
        print(f"DATABASE ERROR: {e}")

if __name__ == "__main__":    
    main()
