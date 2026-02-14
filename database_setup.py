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

def create_tables():
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

        # Drop existing tables to start fresh
        print("Dropping existing tables...")
        cur.execute("DROP TABLE IF EXISTS Projects CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Orders CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Customers CASCADE;")
        cur.execute("DROP TABLE IF EXISTS Employees CASCADE;")

        # Create Customers table
        print("Creating Customers table...")
        cur.execute("""
            CREATE TABLE Customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                city VARCHAR(100),
                created_at DATE DEFAULT CURRENT_DATE
            );
        """)

        # Create Employees table
        print("Creating Employees table...")
        cur.execute("""
            CREATE TABLE Employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                joining_date DATE
            );
        """)

        # Create Projects table
        print("Creating Projects table...")
        cur.execute("""
            CREATE TABLE Projects (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES Employees(id),
                budget NUMERIC(12, 2),
                start_date DATE
            );
        """)

        # Create Orders table
        print("Creating Orders table...")
        cur.execute("""
            CREATE TABLE Orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES Customers(id),
                amount NUMERIC(12, 2),
                order_date DATE
            );
        """)

        conn.commit()
        print("All tables created successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error executing sql: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
