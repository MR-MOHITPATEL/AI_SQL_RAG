
class SchemaAgent:
    def get_schema(self, query: str = "") -> dict:
        """
        Returns the database schema. 
        In a more complex system, this might filter tables based on the query.
        """
        schema = {
            "tables": {
                "Customers": {
                    "columns": [
                        {"name": "id", "type": "SERIAL", "description": "Primary Key"},
                        {"name": "name", "type": "VARCHAR(100)", "description": "Customer Name"},
                        {"name": "email", "type": "VARCHAR(100)", "description": "Unique Email"},
                        {"name": "city", "type": "VARCHAR(100)", "description": "City"},
                        {"name": "created_at", "type": "DATE", "description": "Registration Date"}
                    ]
                },
                "Orders": {
                    "columns": [
                        {"name": "id", "type": "SERIAL", "description": "Primary Key"},
                        {"name": "customer_id", "type": "INTEGER", "description": "Foreign Key to Customers.id"},
                        {"name": "amount", "type": "NUMERIC(12, 2)", "description": "Order Amount"},
                        {"name": "order_date", "type": "DATE", "description": "Date of Order"}
                    ]
                },
                "Employees": {
                    "columns": [
                        {"name": "id", "type": "SERIAL", "description": "Primary Key"},
                        {"name": "name", "type": "VARCHAR(100)", "description": "Employee Name"},
                        {"name": "department", "type": "VARCHAR(100)", "description": "Department (Sales, Engineering, etc.)"},
                        {"name": "joining_date", "type": "DATE", "description": "Date of Joining"}
                    ]
                },
                "Projects": {
                    "columns": [
                        {"name": "id", "type": "SERIAL", "description": "Primary Key"},
                        {"name": "employee_id", "type": "INTEGER", "description": "Foreign Key to Employees.id (Project Lead)"},
                        {"name": "budget", "type": "NUMERIC(12, 2)", "description": "Project Budget"},
                        {"name": "start_date", "type": "DATE", "description": "Project Start Date"}
                    ]
                }
            },
            "relationships": [
                "Orders.customer_id -> Customers.id",
                "Projects.employee_id -> Employees.id"
            ]
        }
        return schema
