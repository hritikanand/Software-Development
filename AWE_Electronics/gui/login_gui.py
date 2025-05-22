import tkinter as tk
from tkinter import messagebox
from utils.file_handler import read_json
from gui.customer_gui import customer_gui
from gui.admin_gui import admin_gui

USER_FILE = "data/users.json"

def login_user(username, password, root):
    users = read_json(USER_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            root.destroy()
            if user['role'] == 'admin':
                admin_gui()
            else:
                customer_gui(user)
            return
    messagebox.showerror("Login Failed", "Invalid credentials.")

def login_gui():
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x200")

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def try_login():
        login_user(username_entry.get(), password_entry.get(), root)

    tk.Button(root, text="Login", command=try_login).pack(pady=10)
    root.mainloop()
