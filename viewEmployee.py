import tkinter as tk
from tkinter import ttk
import sqlite3

class ViewEmployeesWindow:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn

        # View Employee Window
        self.window = tk.Toplevel(parent)
        self.window.title("View Employees")

        # Table (Hindi ko sure ngaa ga blanko ang una nga cell te gin idog ko na lang ang mga headers muna nag start ta sa #1 instead of #0)
        self.tree = ttk.Treeview(self.window, columns=('ID', 'First Name', 'Last Name', 'Employee ID', 'Days Worked', 'Overtime', 'Deductions', 'Gross Salary', 'Net Salary'))
        self.tree.heading('#1', text='ID')
        self.tree.heading('#2', text='First Name')
        self.tree.heading('#3', text='Last Name')
        self.tree.heading('#4', text='Employee ID')
        self.tree.heading('#5', text='Days Worked')
        self.tree.heading('#6', text='Overtime')
        self.tree.heading('#7', text='Deductions')
        self.tree.heading('#8', text='Gross Salary')
        self.tree.heading('#9', text='Net Salary')

        self.tree.pack(expand=True, fill='both')

        # Load employee data
        self.load_employee_data()

    # Diri ang declaration sang rate sang per day nga salary kag ang per hour rate sang overtime
    def calculate_gross_salary(self, days_worked, overtime_hours):
        per_day_salary = 650
        per_hour_overtime_rate = 102

        gross_salary = (days_worked * per_day_salary) + (overtime_hours * per_hour_overtime_rate)
        return gross_salary

    def calculate_net_salary(self, gross_salary, deductions):
        net_salary = gross_salary - deductions
        return net_salary

    def load_employee_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        total_salaries = 0

        for employee in employees:
            # Gross salary kag net salary math
            gross_salary = self.calculate_gross_salary(employee[4], employee[5])
            net_salary = self.calculate_net_salary(gross_salary, employee[6])

            # Update the database with the calculated values
            cursor.execute("UPDATE employees SET gross_salary=?, net_salary=? WHERE id=?", (gross_salary, net_salary, employee[0]))
            self.conn.commit()

            # Ensure the values correspond to the correct columns
            self.tree.insert('', 'end', values=(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], gross_salary, net_salary))

            # Update total salaries
            total_salaries += net_salary

        # Displays the calculated total salary to be paid to all the employees
        self.tree.insert('', 'end', values=('Total Salaries', '', '', '', '', '', '', '', total_salaries))
