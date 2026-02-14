import os
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # Fallback to OPENAI_API_KEY if GEMINI_API_KEY is not set, 
            # to be helpful during migration, or just error out. 
            # Given instructions, better to strict or just look for it.
            # Let's try to look for it, or checking if user put it in OPENAI_API_KEY var by mistake?
            # adheres to strict refactor:
            pass # We will check before config
        
        if not self.api_key:
             raise ValueError("GEMINI_API_KEY environment variable not set")
             
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')


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
        
        full_prompt = f"{system_prompt}\n\nQuestion: {query}"

        try:
            response = self.model.generate_content(full_prompt)
            sql = response.text.strip()
            
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
