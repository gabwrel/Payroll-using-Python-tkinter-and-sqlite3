import tkinter as tk
from tkinter import messagebox
import sqlite3

class AddEmployeeWindow:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn

        # Create the add employee window
        self.window = tk.Toplevel(parent)
        self.window.title("Add Employee")

        # Create and pack entry widgets
        tk.Label(self.window, text="First Name:").pack(pady=5)
        self.first_name_entry = tk.Entry(self.window)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.window, text="Last Name:").pack(pady=5)
        self.last_name_entry = tk.Entry(self.window)
        self.last_name_entry.pack(pady=5)

        tk.Label(self.window, text="Employee ID:").pack(pady=5)
        self.employee_id_entry = tk.Entry(self.window)
        self.employee_id_entry.pack(pady=5)

        tk.Label(self.window, text="Days Worked:").pack(pady=5)
        self.days_worked_entry = tk.Entry(self.window)
        self.days_worked_entry.pack(pady=5)

        tk.Label(self.window, text="Overtime:").pack(pady=5)
        self.overtime_entry = tk.Entry(self.window)
        self.overtime_entry.pack(pady=5)

        tk.Label(self.window, text="Deductions:").pack(pady=5)
        self.deductions_entry = tk.Entry(self.window)
        self.deductions_entry.pack(pady=5)

        # Create and pack the save button
        save_button = tk.Button(self.window, text="Save", command=self.save_employee)
        save_button.pack(pady=10)

    def save_employee(self):
        # Retrieve values from entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        employee_id = self.employee_id_entry.get()
        days_worked = self.days_worked_entry.get()
        overtime = self.overtime_entry.get()
        deductions = self.deductions_entry.get()

        # Perform save logic to SQLite database
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO employees (first_name, last_name, employee_id, days_worked, overtime, deductions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, employee_id, days_worked, overtime, deductions))
        self.conn.commit()

        messagebox.showinfo("Employee Information", "Employee saved successfully.")
        self.window.destroy()  # Close the add employee window
