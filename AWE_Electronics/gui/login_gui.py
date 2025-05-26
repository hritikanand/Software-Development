import tkinter as tk
from tkinter import messagebox
from utils.file_handler import read_json

USER_FILE = "data/users.json"

def login_gui(previous_geometry="1000x700"):
    root = tk.Tk()
    root.title("AWE Electronics - Sign In")
    root.geometry(previous_geometry)
    root.resizable(True, True)
    root.minsize(600, 500)
    
    # Center the window if no previous geometry
    if previous_geometry == "1000x700":
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (500 // 2)
        y = (root.winfo_screenheight() // 2) - (500 // 2)
        root.geometry(f"500x500+{x}+{y}")
    
    # Modern color scheme
    colors = {
        'primary': '#2c3e50',
        'secondary': '#3498db',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'light': '#ecf0f1',
        'white': '#ffffff',
        'text_dark': '#2c3e50',
        'text_light': '#7f8c8d'
    }
    
    root.configure(bg=colors['light'])
    
    # Header section
    header_frame = tk.Frame(root, bg=colors['primary'], height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Back button and title
    header_content = tk.Frame(header_frame, bg=colors['primary'])
    header_content.pack(fill='both', expand=True, padx=20)
    
    def go_back():
        current_geometry = root.geometry()
        root.destroy()
        from gui.start_gui import start_gui
        start_gui()
    
    back_btn = tk.Button(header_content,
                        text="← Back",
                        font=('Segoe UI', 10, 'bold'),
                        bg=colors['secondary'],
                        fg='white',
                        border=0,
                        padx=15,
                        pady=6,
                        cursor='hand2',
                        relief='flat',
                        command=go_back)
    back_btn.pack(side='left', pady=20)
    
    header_title = tk.Label(header_content,
                           text="AWE Electronics",
                           font=('Segoe UI', 16, 'bold'),
                           bg=colors['primary'],
                           fg='white')
    header_title.pack(side='right', pady=20)
    
    # Main content area
    main_frame = tk.Frame(root, bg=colors['light'])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Login card
    card_frame = tk.Frame(main_frame, bg=colors['white'], relief='solid', bd=1)
    card_frame.pack(expand=True, anchor='center', padx=20, pady=10)
    
    # Card content
    content_frame = tk.Frame(card_frame, bg=colors['white'])
    content_frame.pack(fill='both', expand=True, padx=30, pady=30)
    
    # Logo
    logo_frame = tk.Frame(content_frame, bg=colors['success'], width=60, height=60)
    logo_frame.pack(anchor='center')
    logo_frame.pack_propagate(False)
    
    logo_label = tk.Label(logo_frame,
                         text="AWE",
                         font=('Segoe UI', 14, 'bold'),
                         bg=colors['success'],
                         fg='white')
    logo_label.pack(expand=True)
    
    # Title
    title_label = tk.Label(content_frame,
                          text="Welcome Back!",
                          font=('Segoe UI', 20, 'bold'),
                          bg=colors['white'],
                          fg=colors['text_dark'])
    title_label.pack(pady=(15, 5))
    
    # Subtitle
    subtitle_label = tk.Label(content_frame,
                             text="Sign in to your account to continue",
                             font=('Segoe UI', 11),
                             bg=colors['white'],
                             fg=colors['text_light'])
    subtitle_label.pack(pady=(0, 20))
    
    # Form fields
    # Username field
    username_label = tk.Label(content_frame,
                             text="Username",
                             font=('Segoe UI', 11, 'bold'),
                             bg=colors['white'],
                             fg=colors['text_dark'])
    username_label.pack(anchor='w', pady=(0, 5))
    
    username_entry = tk.Entry(content_frame,
                             font=('Segoe UI', 11),
                             relief='solid',
                             bd=2,
                             bg=colors['white'])
    username_entry.pack(fill='x', ipady=8, pady=(0, 15))
    
    # Password field
    password_label = tk.Label(content_frame,
                             text="Password",
                             font=('Segoe UI', 11, 'bold'),
                             bg=colors['white'],
                             fg=colors['text_dark'])
    password_label.pack(anchor='w', pady=(0, 5))
    
    password_entry = tk.Entry(content_frame,
                             font=('Segoe UI', 11),
                             relief='solid',
                             bd=2,
                             show="*",
                             bg=colors['white'])
    password_entry.pack(fill='x', ipady=8, pady=(0, 20))
    
    # Focus effects
    def on_entry_focus_in(event, entry):
        entry.config(bd=3, relief='solid')
    
    def on_entry_focus_out(event, entry):
        entry.config(bd=2, relief='solid')
    
    username_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(e, username_entry))
    username_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(e, username_entry))
    password_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(e, password_entry))
    password_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(e, password_entry))
    
    # Status label for login feedback
    status_label = tk.Label(content_frame,
                           text="",
                           font=('Segoe UI', 9),
                           bg=colors['white'],
                           fg=colors['danger'])
    status_label.pack(pady=(0, 10))
    
    # Login function with better error handling
    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        # Clear previous status
        status_label.config(text="", fg=colors['danger'])
        
        if not username or not password:
            status_label.config(text="⚠️ Please fill in all fields!", fg=colors['warning'])
            return
        
        # Show loading
        status_label.config(text="🔄 Signing in...", fg=colors['secondary'])
        root.update()
        
        try:
            users = read_json(USER_FILE)
            
            if not users:
                status_label.config(text="❌ No user data found. Please contact support.", fg=colors['danger'])
                return
            
            # Find user
            user_found = None
            for user in users:
                if user.get('username') == username and user.get('password') == password:
                    user_found = user
                    break
            
            if user_found:
                # Successful login
                status_label.config(text="✅ Login successful!", fg=colors['success'])
                root.update()
                
                messagebox.showinfo("Login Successful", 
                                  f"Welcome back, {username}!\n\n"
                                  f"Role: {user_found.get('role', 'user').title()}")
                
                current_geometry = root.geometry()
                root.destroy()
                
                # Route to appropriate interface
                if user_found.get('role') == 'admin':
                    from gui.admin_gui import admin_gui
                    admin_gui(current_geometry)
                else:
                    from gui.customer_gui import customer_gui
                    customer_gui(user_found, current_geometry)
                return
            else:
                # Login failed
                status_label.config(text="❌ Invalid username or password!", fg=colors['danger'])
                password_entry.delete(0, tk.END)
                username_entry.focus()
                
        except Exception as e:
            status_label.config(text="❌ Login error occurred!", fg=colors['danger'])
            print(f"Login error: {e}")  # For debugging
    
    # Login button
    login_btn = tk.Button(content_frame,
                         text="🔐 SIGN IN",
                         font=('Segoe UI', 12, 'bold'),
                         bg=colors['success'],
                         fg='white',
                         border=0,
                         padx=30,
                         pady=10,
                         cursor='hand2',
                         relief='flat',
                         command=attempt_login)
    login_btn.pack(fill='x', pady=(0, 15))
    
    # Hover effects for login button
    def on_login_enter(e):
        login_btn.configure(bg='#219a52')
    
    def on_login_leave(e):
        login_btn.configure(bg=colors['success'])
    
    login_btn.bind("<Enter>", on_login_enter)
    login_btn.bind("<Leave>", on_login_leave)
    
    # Divider
    divider = tk.Frame(content_frame, bg=colors['light'], height=1)
    divider.pack(fill='x', pady=10)
    
    # Register link
    register_frame = tk.Frame(content_frame, bg=colors['white'])
    register_frame.pack(fill='x')
    
    register_text = tk.Label(register_frame,
                           text="Don't have an account?",
                           font=('Segoe UI', 10),
                           bg=colors['white'],
                           fg=colors['text_light'])
    register_text.pack()
    
    def open_register():
        current_geometry = root.geometry()
        root.destroy()
        from gui.register_gui import register_gui
        register_gui(current_geometry)
    
    register_link = tk.Label(register_frame,
                           text="Create New Account",
                           font=('Segoe UI', 10, 'bold', 'underline'),
                           bg=colors['white'],
                           fg=colors['secondary'],
                           cursor='hand2')
    register_link.pack()
    register_link.bind("<Button-1>", lambda e: open_register())
    
    # Footer info
    footer_label = tk.Label(content_frame,
                           text="🔒 Secure login with validation",
                           font=('Segoe UI', 8),
                           bg=colors['white'],
                           fg=colors['text_light'])
    footer_label.pack(pady=(10, 0))
    
    # Status bar
    status_frame = tk.Frame(root, bg=colors['light'], height=25)
    status_frame.pack(fill='x', side='bottom')
    status_frame.pack_propagate(False)
    
    status_bar_label = tk.Label(status_frame,
                               text="Press Enter to login • Press Escape to go back",
                               font=('Segoe UI', 8),
                               bg=colors['light'],
                               fg=colors['text_light'])
    status_bar_label.pack(expand=True)
    
    # Keyboard shortcuts
    root.bind('<Return>', lambda event: attempt_login())
    root.bind('<Escape>', lambda event: go_back())
    
    # Focus on username entry
    root.after(100, lambda: username_entry.focus())
    
    # Window close handler
    def on_closing():
        go_back()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    login_gui()