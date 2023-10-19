import sqlite3

# Nag gamit ko REAL instead of int sa mga salary kag sa deductions kay basi may decimal numbers
def create_employee_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            employee_id TEXT,
            days_worked INTEGER,
            overtime INTEGER,
            deductions REAL,
            gross_salary REAL,
            net_salary REAL
        )
    ''')
    conn.commit()
