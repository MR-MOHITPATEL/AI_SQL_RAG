import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
             raise ValueError("GROQ_API_KEY environment variable not set")
             
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = "openai/gpt-oss-120b" # As requested

    def generate_sql(self, query: str, schema: dict) -> str:
        """
        Generates a SQL query from a natural language query using the provided schema.
        """
        current_date = datetime.date.today()
        
        system_prompt = f"""
        You are an expert PostgreSQL Data Analyst.
        Given the following database schema and a natural language user request, generate a valid PostgreSQL query.
        
        Schema:
        {schema}
        
        Current Date: {current_date}
        
        Rules:
        1. Return ONLY the raw SQL query. Do not use markdown code blocks (```sql ... ```).
        2. Do not provide any explanation.
        3. Use standard PostgreSQL syntax.
        4. Handle case-insensitive matching for string literals using ILIKE if appropriate.
        5. For temporal queries like "last year", "last month", use the Current Date as reference.
           - "last year" means the previous calendar year.
           - "last month" means the previous calendar month.
        6. Always alias tables appropriately (e.g., c for Customers, o for Orders).
        7. If the user request is a greeting (e.g., "hi", "hello"), asking for identity, or NOT related to the database schema, return ONLY the string "NO_QUERY".
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.1
            )
            
            sql = response.choices[0].message.content.strip()
            
            # Sanitization in case the model ignores the "no markdown" rule
            if sql.startswith("```sql"):
                sql = sql[6:]
            if sql.startswith("```"):
                sql = sql[3:]
            if sql.endswith("```"):
                sql = sql[:-3]
                
            return sql.strip()

        except Exception as e:
            raise Exception(f"Failed to generate SQL: {str(e)}")
