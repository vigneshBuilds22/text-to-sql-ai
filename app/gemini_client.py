from google import genai
from google.genai import types
PROJECT_ID = "ai-innovation-lab-506906"
LOCATION = "us-central1"
MODEL = "gemini-2.5-flash"
client =genai.Client(vertexai = True,
                     project=PROJECT_ID,
                     location=LOCATION
)
def generate_Sql(question, schema):
    prompt = f"""
You are an expert SQLite SQL generator.

Your task is to convert the user's natural-language question into
ONE valid, read-only SQLite SQL query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

IMPORTANT RULES:
1. Understand ALL parts of the user's question.
2. If the user asks for multiple pieces of information, the SQL query
   must return all requested information.
3. Return ONLY the SQL query.
4. Do not use markdown code fences.
5. Do not explain the query.
6. Use only tables and columns that exist in the database schema.
7. Generate valid SQLite SQL.
8. Only generate SELECT queries.
9. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or other
   database-modifying statements.
10. Prefer a single SQL query that returns all requested information.

EXAMPLES:

Question:
Which customer has placed the most orders?

SQL:
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY order_count DESC
LIMIT 1;

Question:
How many customers are there and list their names?

SQL:
SELECT name, COUNT(*) OVER () AS total_customers
FROM customers;

Now generate the SQL for the user's question.

SQL:
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
        ),
    )

    return response.text.strip()
