import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ViewEmployeesWindow:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn

        # View Employee Window
        self.window = tk.Toplevel(parent)
        self.window.title("View Employees")

        self.search_frame = tk.Frame(self.window)
        self.search_entry = tk.Entry(self.search_frame)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_employee)
        self.search_entry.pack(side=tk.LEFT)
        self.search_button.pack(side=tk.LEFT)
        self.search_frame.pack(pady=10)

        # Table
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

        # Call the load_employee_data method
        self.load_employee_data()

    def load_employee_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for employee in employees:
            gross_salary = self.calculate_gross_salary(employee[4], employee[5])
            net_salary = self.calculate_net_salary(gross_salary, employee[6])

            self.tree.insert('', 'end', values=(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], gross_salary, net_salary))

        # Adjust column widths based on content
        for col in self.tree["columns"]:
            self.tree.column(col, width=tk.ALL)


    def calculate_gross_salary(self, days_worked, overtime_hours):
        per_day_salary = 650
        per_hour_overtime_rate = 102

        gross_salary = (days_worked * per_day_salary) + (overtime_hours * per_hour_overtime_rate)
        return gross_salary

    def calculate_net_salary(self, gross_salary, deductions):
        net_salary = gross_salary - deductions
        return net_salary

    def search_employee(self):
        search_term = self.search_entry.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE first_name LIKE ? OR last_name LIKE ? OR employee_id LIKE ?", ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        employees = cursor.fetchall()

        total_salaries = 0

        for employee in employees:
            gross_salary = self.calculate_gross_salary(employee[4], employee[5])
            net_salary = self.calculate_net_salary(gross_salary, employee[6])

            cursor.execute("UPDATE employees SET gross_salary=?, net_salary=? WHERE id=?", (gross_salary, net_salary, employee[0]))
            self.conn.commit()

            self.tree.insert('', 'end', values=(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], gross_salary, net_salary))

            total_salaries += net_salary

        self.tree.insert('', 'end', values=('Total Salaries', '', '', '', '', '', '', '', total_salaries))

