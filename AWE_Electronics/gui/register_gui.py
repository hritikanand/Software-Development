# gui/register_gui.py
import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from utils.file_handler import read_json, write_json

USER_FILE = "data/users.json"

def register_gui():
    root = tk.Tk()
    root.title("Register")
    root.geometry("300x350")

    fields = ["Username", "Password", "Email", "Address", "Phone Number"]
    entries = {}

    for field in fields:
        tk.Label(root, text=field).pack()
        entry = tk.Entry(root, show="*" if field == "Password" else None)
        entry.pack()
        entries[field] = entry

    def register():
        users = read_json(USER_FILE)
        username = entries["Username"].get()

        if any(u['username'] == username for u in users):
            messagebox.showerror("Error", "Username already exists.")
            return

        new_cust = Customer(
            username=username,
            password=entries["Password"].get(),
            email=entries["Email"].get(),
            address=entries["Address"].get(),
            phone_number=entries["Phone Number"].get()
        )
        users.append(new_cust.to_dict())
        write_json(USER_FILE, users)
        messagebox.showinfo("Success", "Account created!")
        root.destroy()

    tk.Button(root, text="Register", command=register).pack(pady=10)
    root.mainloop()
