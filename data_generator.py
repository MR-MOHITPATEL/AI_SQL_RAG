import os
import psycopg2
import random
from faker import Faker
from dotenv import load_dotenv
from psycopg2 import extras

load_dotenv()

fake = Faker()

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "rag_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "kjs2026")
DB_PORT = os.getenv("DB_PORT", "5432")

def generate_data():
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

        print("Generating synthetic data...")

        # 1. Customers (350)
        customers = []
        for _ in range(350):
            customers.append((
                fake.name(),
                fake.unique.email(),
                fake.city(),
                fake.date_between(start_date='-2y', end_date='today')
            ))
        
        extras.execute_batch(cur, """
            INSERT INTO Customers (name, email, city, created_at) VALUES (%s, %s, %s, %s)
        """, customers)
        print(f"Inserted {len(customers)} customers.")

        # 2. Employees (50)
        employees = []
        departments = ['Sales', 'Engineering', 'HR', 'Marketing', 'Support']
        for _ in range(50):
            employees.append((
                fake.name(),
                random.choice(departments),
                fake.date_between(start_date='-5y', end_date='today')
            ))

        extras.execute_batch(cur, """
            INSERT INTO Employees (name, department, joining_date) VALUES (%s, %s, %s)
        """, employees)
        print(f"Inserted {len(employees)} employees.")
        
        # Get Employee IDs for Projects
        cur.execute("SELECT id FROM Employees;")
        emp_ids = [row[0] for row in cur.fetchall()]

        # 3. Projects (150)
        projects = []
        for _ in range(150):
            projects.append((
                random.choice(emp_ids),
                round(random.uniform(5000, 100000), 2),
                fake.date_between(start_date='-1y', end_date='today')
            ))
        
        extras.execute_batch(cur, """
            INSERT INTO Projects (employee_id, budget, start_date) VALUES (%s, %s, %s)
        """, projects)
        print(f"Inserted {len(projects)} projects.")

        # Get Customer IDs for Orders
        cur.execute("SELECT id FROM Customers;")
        cust_ids = [row[0] for row in cur.fetchall()]

        # 4. Orders (1200)
        orders = []
        for _ in range(1200):
            orders.append((
                random.choice(cust_ids),
                round(random.uniform(20, 2000), 2),
                fake.date_between(start_date='-1y', end_date='today')
            ))
        
        extras.execute_batch(cur, """
            INSERT INTO Orders (customer_id, amount, order_date) VALUES (%s, %s, %s)
        """, orders)
        print(f"Inserted {len(orders)} orders.")

        conn.commit()
        print("Data generation complete.")
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    generate_data()
