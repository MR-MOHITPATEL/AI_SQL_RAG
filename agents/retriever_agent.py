import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "rag_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = os.getenv("DB_PORT", "5432")

class RetrieverAgent:
    def execute_query(self, sql: str) -> dict:
        """
        Executes a SQL query and returns the results.
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            cur = conn.cursor()
            cur = conn.cursor()
            
            dangerous_keywords = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE"]

            if any(keyword in sql.upper() for keyword in dangerous_keywords):
                cur.close()
                return {"columns": [], "rows": [], "error": "Unsafe SQL detected"}

            cur.execute(sql)
            
            # Fetch execution results
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                results = [dict(zip(columns, row)) for row in rows]
            else:
                results = []
                columns = []
            
            cur.close()
            return {"columns": columns, "rows": results, "error": None}
            
        except psycopg2.Error as e:
            return {"columns": [], "rows": [], "error": str(e)}
        except Exception as e:
            return {"columns": [], "rows": [], "error": f"Unexpected error: {str(e)}"}
        finally:
            if conn is not None:
                conn.close()
