import tkinter as tk
from tkinter import messagebox
from addEmployee import AddEmployeeWindow
from viewEmployee import ViewEmployeesWindow
from database import create_employee_table
import sqlite3

def login():
    # sa valid_users pwede man dugangan ang user through muni nga
    # pag declare
    # valid_users = {"admin": "admin", "username", "password"}
    valid_users = {"admin": "admin", "username": "password"}

    entered_username = username_entry.get()
    entered_password = password_entry.get()

    # Login authentication
    if entered_username in valid_users and entered_password == valid_users[entered_username]:
        welcome_message = f"Hello, {entered_username}! Welcome!"
        messagebox.showinfo("Welcome", welcome_message)
        create_main_menu()
    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")

# Gin import ni siya halin sa addEmployee.py
def add_employee():
    AddEmployeeWindow(root, conn)

# Gin import ni halin sa viewEmployee.py
def view_employees():
    ViewEmployeesWindow(root, conn)

def create_main_menu():
    # Kung makalogin na, ang code sa dalom ang matago sang login nga window
    root.withdraw()

    # Main menu window
    main_menu = tk.Tk()
    main_menu.title("Main Menu")

    add_employee_button = tk.Button(main_menu, text="Add Employee", command=add_employee)
    add_employee_button.pack(pady=10)

    view_employees_button = tk.Button(main_menu, text="View Employees", command=view_employees)
    view_employees_button.pack(pady=10)

    main_menu.mainloop()

# Code para mag connect sa aton database (database.py)
conn = sqlite3.connect('employee_database.db')
create_employee_table(conn)

# Welcome Screen Window
root = tk.Tk()
root.title("Welcome Screen")

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

root.mainloop()

# Code para i close ang connection sa database kung gin close ang app
conn.close()
