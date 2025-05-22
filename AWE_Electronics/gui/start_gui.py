# gui/start_gui.py

import tkinter as tk
from gui.login_gui import login_gui
from gui.register_gui import register_gui

def start_gui():
    root = tk.Tk()
    root.title("AWE Electronics")
    root.geometry("300x200")

    tk.Label(root, text="Welcome to AWE Electronics!", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Login", width=20, command=lambda: [root.destroy(), login_gui()]).pack(pady=5)
    tk.Button(root, text="Register", width=20, command=lambda: [root.destroy(), register_gui()]).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
