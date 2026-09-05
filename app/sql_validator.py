import re
def validate_sql(sql):
    """Validate AI generated sql query before execution.
    only read-only sql queries are allowed.
    """
    if not sql:
        raise ValueError("SQL query is empty.")
    #remove leading/trailing whitespaces
    sql =sql.strip()
    #remove markdown fences if gemini returns them
    sql = re.sub(r"^```sql\s*","",sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*","",sql)
    sql = re.sub(r"\s*```$","",sql)
    sql=sql.strip()

    #only select statements are allowed
    if not sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed.")
    #Block potentially dangerous keywords
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
    for keyword in forbidden_keywords:
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, sql, re.IGNORECASE):
            raise ValueError(f"Forbidden keyword detected in sql query: {keyword}")
        
    return sql
