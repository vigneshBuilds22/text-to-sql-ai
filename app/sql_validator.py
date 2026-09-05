import re


def validate_sql(sql):
    """
    Validate AI-generated SQL before execution.

    Only read-only SQL queries are allowed.
    """

    if not sql:
        raise ValueError("SQL query is empty.")

    # Remove leading/trailing whitespace
    sql = sql.strip()

    # Remove markdown code fences if Gemini returns them
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)
    sql = sql.strip()

    # Remove one trailing semicolon
    sql = sql.rstrip(";").strip()

    # Only SELECT or WITH queries are allowed
    if not re.match(r"^(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT or WITH queries are allowed.")

    # Prevent multiple SQL statements
    if ";" in sql:
        raise ValueError("Multiple SQL statements are not allowed.")

    # Block potentially dangerous SQL operations
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
    ]

    for keyword in forbidden_keywords:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql, re.IGNORECASE):
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    return sql
