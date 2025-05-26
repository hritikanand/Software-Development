import tkinter as tk
from tkinter import messagebox
from utils.file_handler import initialize_default_data

def start_gui():
    # Initialize default data files
    initialize_default_data()
    
    root = tk.Tk()
    root.title("AWE Electronics - Welcome")
    root.geometry("1000x700")
    root.resizable(True, True)
    root.minsize(800, 600)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1000 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"1000x700+{x}+{y}")
    
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
    
    # Main container with better proportions
    main_container = tk.Frame(root, bg=colors['white'])
    main_container.pack(fill='both', expand=True, padx=30, pady=30)
    
    # Header section with modern design
    header_frame = tk.Frame(main_container, bg=colors['primary'], height=120)
    header_frame.pack(fill='x', pady=(0, 20))
    header_frame.pack_propagate(False)
    
    # Logo and title in header
    header_content = tk.Frame(header_frame, bg=colors['primary'])
    header_content.pack(expand=True)
    
    # Logo
    logo_frame = tk.Frame(header_content, bg=colors['white'], width=80, height=80)
    logo_frame.pack(pady=20)
    logo_frame.pack_propagate(False)
    
    logo_label = tk.Label(logo_frame, 
                         text="AWE", 
                         font=('Segoe UI', 20, 'bold'), 
                         bg=colors['white'], 
                         fg=colors['primary'])
    logo_label.pack(expand=True)
    
    # Content area
    content_frame = tk.Frame(main_container, bg=colors['white'])
    content_frame.pack(fill='both', expand=True)
    
    # Welcome section
    welcome_frame = tk.Frame(content_frame, bg=colors['white'])
    welcome_frame.pack(fill='x', pady=20)
    
    # Main title
    title_label = tk.Label(welcome_frame, 
                          text="Welcome to AWE Electronics",
                          font=('Segoe UI', 24, 'bold'),
                          bg=colors['white'],
                          fg=colors['text_dark'])
    title_label.pack(pady=(0, 8))
    
    # Subtitle
    subtitle_label = tk.Label(welcome_frame,
                             text="Your Premier Electronics Store",
                             font=('Segoe UI', 14),
                             bg=colors['white'],
                             fg=colors['secondary'])
    subtitle_label.pack(pady=(0, 8))
    
    # Description
    description_label = tk.Label(welcome_frame,
                                text="Discover amazing electronics, shop with confidence,\nand enjoy exceptional customer service.",
                                font=('Segoe UI', 11),
                                bg=colors['white'],
                                fg=colors['text_light'],
                                justify='center')
    description_label.pack(pady=(0, 20))
    
    # Buttons container with better spacing
    buttons_container = tk.Frame(content_frame, bg=colors['white'])
    buttons_container.pack(fill='x', padx=50, pady=20)
    
    # Button creation function with hover effects
    def create_button(parent, text, bg_color, command, icon=""):
        btn = tk.Button(parent,
                       text=f"{icon} {text}",
                       font=('Segoe UI', 12, 'bold'),
                       bg=bg_color,
                       fg='white',
                       border=0,
                       padx=30,
                       pady=12,
                       cursor='hand2',
                       relief='flat',
                       command=command)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=darken_color(bg_color))
        
        def on_leave(e):
            btn.configure(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def darken_color(color):
        color_map = {
            colors['success']: '#219a52',
            colors['secondary']: '#2980b9',
            colors['warning']: '#e67e22',
            colors['primary']: '#1a252f'
        }
        return color_map.get(color, color)
    
    # Store geometry function
    def get_current_geometry():
        return root.geometry()
    
    # Login button
    def open_login():
        current_geometry = get_current_geometry()
        root.destroy()
        from gui.login_gui import login_gui
        login_gui(current_geometry)
    
    login_btn = create_button(buttons_container, "SIGN IN", colors['success'], open_login, "🔐")
    login_btn.pack(fill='x', pady=(0, 12))
    
    # Register button
    def open_register():
        current_geometry = get_current_geometry()
        root.destroy()
        from gui.register_gui import register_gui
        register_gui(current_geometry)
    
    register_btn = create_button(buttons_container, "CREATE ACCOUNT", colors['secondary'], open_register, "📝")
    register_btn.pack(fill='x', pady=(0, 12))
    
    # Guest button
    def guest_login():
        response = messagebox.askquestion("Guest Mode", 
                                        "Continue as guest?\n\n"
                                        "Note: You can browse products but will need to "
                                        "create an account to make purchases.",
                                        icon='question')
        if response == 'yes':
            guest_user = {
                "username": "Guest User",
                "role": "customer",
                "cart": []
            }
            current_geometry = get_current_geometry()
            root.destroy()
            from gui.customer_gui import customer_gui
            customer_gui(guest_user, current_geometry)
    
    guest_btn = create_button(buttons_container, "CONTINUE AS GUEST", colors['warning'], guest_login, "👤")
    guest_btn.pack(fill='x', pady=(0, 20))
    
    # Features section with better layout
    features_frame = tk.Frame(content_frame, bg=colors['light'], relief='solid', bd=1)
    features_frame.pack(fill='x', padx=30, pady=(10, 20))
    
    features_title = tk.Label(features_frame,
                             text="Why Choose AWE Electronics?",
                             font=('Segoe UI', 14, 'bold'),
                             bg=colors['light'],
                             fg=colors['text_dark'])
    features_title.pack(pady=12)
    
    # Features grid
    features_container = tk.Frame(features_frame, bg=colors['light'])
    features_container.pack(fill='x', padx=20, pady=(0, 12))
    
    features = [
        "🛍️ Wide range of quality electronics",
        "💳 Secure online payments",
        "🚚 Fast nationwide delivery", 
        "🔒 Safe and secure shopping",
        "💎 Premium customer service"
    ]
    
    for i, feature in enumerate(features):
        feature_label = tk.Label(features_container,
                               text=feature,
                               font=('Segoe UI', 10),
                               bg=colors['light'],
                               fg=colors['text_dark'])
        feature_label.pack(pady=1)
    
    # Login credentials info
    info_frame = tk.Frame(content_frame, bg=colors['white'])
    info_frame.pack(fill='x', pady=(0, 10))
    
    def show_login_info():
        messagebox.showinfo("Login Information", 
                           "Available Login Credentials:\n\n"
                           "👨‍💼 Admin Account:\n"
                           "Username: admin\n"
                           "Password: admin123\n\n"
                           "👤 Customer Accounts:\n"
                           "Username: customer1\n"
                           "Password: customer123\n\n"
                           "Username: saqib\n"
                           "Password: saqib1")
    
    info_btn = tk.Button(info_frame,
                        text="ℹ️ View Login Credentials",
                        font=('Segoe UI', 10),
                        bg=colors['white'],
                        fg=colors['secondary'],
                        border=0,
                        cursor='hand2',
                        relief='flat',
                        command=show_login_info)
    info_btn.pack()
    
    # Admin access
    admin_frame = tk.Frame(content_frame, bg=colors['white'])
    admin_frame.pack(fill='x', pady=(5, 10))
    
    admin_link = tk.Label(admin_frame,
                         text="Staff/Admin Login",
                         font=('Segoe UI', 9, 'underline'),
                         bg=colors['white'],
                         fg=colors['text_light'],
                         cursor='hand2')
    admin_link.pack()
    admin_link.bind("<Button-1>", lambda e: open_login())
    
    # Footer
    footer_frame = tk.Frame(content_frame, bg=colors['white'])
    footer_frame.pack(fill='x', pady=(10, 0))
    
    footer_label = tk.Label(footer_frame,
                           text="© 2024 AWE Electronics - Quality Electronics Since 1995",
                           font=('Segoe UI', 8),
                           bg=colors['white'],
                           fg=colors['text_light'])
    footer_label.pack()
    
    # Status bar
    status_frame = tk.Frame(root, bg=colors['light'], height=25)
    status_frame.pack(fill='x', side='bottom')
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(status_frame,
                           text="💡 Press Enter for Quick Login • F1 for Help",
                           font=('Segoe UI', 9),
                           bg=colors['light'],
                           fg=colors['text_light'])
    status_label.pack(expand=True)
    
    # Keyboard shortcuts
    root.bind('<Return>', lambda e: open_login())
    root.bind('<F1>', lambda e: show_login_info())
    root.bind('<Escape>', lambda e: root.quit())
    
    # Exit function
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit AWE Electronics?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    start_gui()