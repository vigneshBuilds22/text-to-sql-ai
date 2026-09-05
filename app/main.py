import sqlite3

from app.gemini_client import generate_Sql, correct_sql
from app.sql_validator import validate_sql
from app.database import execute_query
from app.query_guard import validate_question


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

    question = input("Enter your question about your data: ")

    # Validate user question
    try:
        question = validate_question(question)
    except ValueError as error:
        print(f"Question rejected: {error}")
        return

    # Get database schema
    schema = get_schema()

    print("DATABASE SCHEMA:")
    print(schema)

    # Generate SQL
    print("Generating SQL query...")

    sql_query = generate_Sql(question, schema)

    print("Generated SQL query:")
    print(sql_query)

    # Validate generated SQL
    print("Validating SQL query...")

    try:
        sql = validate_sql(sql_query)
        print("SQL Validation Successful")

    except ValueError as error:
        print(f"SQL Validation Failed: {error}")
        return

    # Execute SQL
    print("Executing SQL query...")

    try:
        columns, rows = execute_query(sql)

        print("Query executed successfully.")
        print("Results:")

        for row in rows:
            print(row)

    except Exception as error:

        print(f"DATABASE ERROR: {error}")
        print("Attempting to correct the SQL query...")

        # Ask Gemini to correct the failed SQL
        corrected_sql = correct_sql(
            question,
            schema,
            sql,
            str(error)
        )

        print("Corrected SQL query:")
        print(corrected_sql)

        # Validate corrected SQL before execution
        print("Validating corrected SQL query...")

        try:
            corrected_sql = validate_sql(corrected_sql)
            print("Corrected SQL Validation Successful")

        except ValueError as validation_error:
            print(
                f"Corrected SQL Validation Failed: {validation_error}"
            )
            return

        # Execute corrected SQL
        print("Executing corrected SQL query...")

        try:
            columns, rows = execute_query(corrected_sql)

            print("Corrected query executed successfully.")
            print("Results:")

            for row in rows:
                print(row)

        except Exception as retry_error:
            print(
                f"Corrected SQL also failed: {retry_error}"
            )


if __name__ == "__main__":
    main()