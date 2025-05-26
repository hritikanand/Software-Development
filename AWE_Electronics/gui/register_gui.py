import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from utils.file_handler import read_json, write_json
import re

USER_FILE = "data/users.json"

def register_gui(previous_geometry="1000x700"):
    root = tk.Tk()
    root.title("AWE Electronics - Create Account")
    root.geometry(previous_geometry)
    root.resizable(True, True)
    root.minsize(600, 500)
    
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
    header_frame = tk.Frame(root, bg=colors['primary'], height=70)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Header content
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
    back_btn.pack(side='left', pady=15)
    
    header_title = tk.Label(header_content,
                           text="AWE Electronics",
                           font=('Segoe UI', 16, 'bold'),
                           bg=colors['primary'],
                           fg='white')
    header_title.pack(side='right', pady=15)
    
    # Main container with scrolling
    main_canvas = tk.Canvas(root, bg=colors['light'], highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    
    # Scrollable frame container
    scroll_container = tk.Frame(main_canvas, bg=colors['light'])
    
    # Configure scrolling
    scroll_container.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )
    
    main_canvas.create_window((0, 0), window=scroll_container, anchor="nw")
    main_canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack canvas and scrollbar
    main_canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")
    
    # Content frame
    content_frame = tk.Frame(scroll_container, bg=colors['white'], relief='solid', bd=1)
    content_frame.pack(anchor='center', pady=15, padx=20)
    
    # Card content
    card_content = tk.Frame(content_frame, bg=colors['white'])
    card_content.pack(fill='both', expand=True, padx=25, pady=25)
    
    # Logo
    logo_frame = tk.Frame(card_content, bg=colors['success'], width=50, height=50)
    logo_frame.pack(anchor='center')
    logo_frame.pack_propagate(False)
    
    logo_label = tk.Label(logo_frame,
                         text="AWE",
                         font=('Segoe UI', 12, 'bold'),
                         bg=colors['success'],
                         fg='white')
    logo_label.pack(expand=True)
    
    # Title
    title_label = tk.Label(card_content,
                          text="Join AWE Electronics!",
                          font=('Segoe UI', 18, 'bold'),
                          bg=colors['white'],
                          fg=colors['text_dark'])
    title_label.pack(pady=(12, 5))
    
    # Subtitle
    subtitle_label = tk.Label(card_content,
                             text="Create your account to start shopping",
                             font=('Segoe UI', 10),
                             bg=colors['white'],
                             fg=colors['text_light'])
    subtitle_label.pack(pady=(0, 15))
    
    # Form fields
    entries = {}
    validation_labels = {}
    
    fields = [
        ("Username", "username", "Choose a unique username (3+ characters)"),
        ("Password", "password", "Minimum 6 characters"),
        ("Confirm Password", "confirm_password", "Re-enter your password"),
        ("Email Address", "email", "Enter a valid email address"),
        ("Full Name", "full_name", "Your first and last name"),
        ("Address", "address", "Street address, City, State, Postal Code"),
        ("Phone Number", "phone", "Include area code (e.g., +61 400 000 000)")
    ]
    
    def create_field(parent, label_text, field_name, placeholder):
        # Field container
        field_frame = tk.Frame(parent, bg=colors['white'])
        field_frame.pack(fill='x', pady=(0, 8))
        
        # Label
        label = tk.Label(field_frame,
                        text=f"{label_text} *",
                        font=('Segoe UI', 9, 'bold'),
                        bg=colors['white'],
                        fg=colors['text_dark'])
        label.pack(anchor='w')
        
        # Entry
        entry = tk.Entry(field_frame, 
                        font=('Segoe UI', 9),
                        relief='solid',
                        bd=1,
                        bg=colors['white'])
        
        if 'password' in field_name.lower():
            entry.configure(show="*")
        
        entry.pack(fill='x', ipady=5, pady=(2, 0))
        
        # Placeholder text
        placeholder_label = tk.Label(field_frame,
                                   text=placeholder,
                                   font=('Segoe UI', 7),
                                   bg=colors['white'],
                                   fg='#95a5a6')
        placeholder_label.pack(anchor='w')
        
        # Validation label
        validation_label = tk.Label(field_frame,
                                   text="",
                                   font=('Segoe UI', 7),
                                   bg=colors['white'],
                                   fg=colors['danger'])
        validation_label.pack(anchor='w')
        
        entries[field_name] = entry
        validation_labels[field_name] = validation_label
        
        return entry
    
    # Create all form fields
    for label_text, field_name, placeholder in fields:
        create_field(card_content, label_text, field_name, placeholder)
    
    # Real-time validation
    def validate_single_field(field_name):
        value = entries[field_name].get().strip()
        validation_label = validation_labels[field_name]
        
        if field_name == "username":
            if len(value) < 3:
                validation_label.config(text="⚠️ Username must be at least 3 characters", fg=colors['warning'])
                return False
            else:
                validation_label.config(text="✅ Looks good", fg=colors['success'])
                return True
                
        elif field_name == "password":
            if len(value) < 6:
                validation_label.config(text="⚠️ Password must be at least 6 characters", fg=colors['warning'])
                return False
            else:
                validation_label.config(text="✅ Good password", fg=colors['success'])
                return True
                
        elif field_name == "confirm_password":
            password = entries["password"].get()
            if value != password:
                validation_label.config(text="⚠️ Passwords do not match", fg=colors['danger'])
                return False
            elif value and len(value) >= 6:
                validation_label.config(text="✅ Passwords match", fg=colors['success'])
                return True
                
        elif field_name == "email":
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                validation_label.config(text="⚠️ Please enter a valid email", fg=colors['warning'])
                return False
            else:
                validation_label.config(text="✅ Valid email", fg=colors['success'])
                return True
                
        elif field_name == "phone":
            phone_clean = re.sub(r'[^\d+]', '', value)
            if len(phone_clean) < 10:
                validation_label.config(text="⚠️ Please enter a valid phone number", fg=colors['warning'])
                return False
            else:
                validation_label.config(text="✅ Valid phone", fg=colors['success'])
                return True
                
        elif field_name in ["full_name", "address"]:
            if len(value) < 2:
                validation_label.config(text=f"⚠️ {field_name.replace('_', ' ').title()} is required", fg=colors['warning'])
                return False
            else:
                validation_label.config(text="✅ Looks good", fg=colors['success'])
                return True
        
        return True
    
    # Add validation to entries
    for field_name, entry in entries.items():
        entry.bind('<KeyRelease>', lambda e, fn=field_name: validate_single_field(fn))
        entry.bind('<FocusOut>', lambda e, fn=field_name: validate_single_field(fn))
    
    # Terms and conditions
    terms_frame = tk.Frame(card_content, bg=colors['light'], relief='solid', bd=1)
    terms_frame.pack(fill='x', pady=10)
    
    terms_var = tk.BooleanVar()
    
    terms_check = tk.Checkbutton(terms_frame,
                               text="I agree to the Terms of Service and Privacy Policy",
                               variable=terms_var,
                               font=('Segoe UI', 8),
                               bg=colors['light'],
                               wraplength=350,
                               justify='left')
    terms_check.pack(padx=8, pady=8)
    
    # Status label for registration feedback
    status_label = tk.Label(card_content,
                           text="",
                           font=('Segoe UI', 9),
                           bg=colors['white'],
                           fg=colors['danger'])
    status_label.pack(pady=(5, 0))
    
    # Registration function
    def attempt_register():
        # Clear previous status
        status_label.config(text="", fg=colors['danger'])
        
        # Basic validation
        all_valid = True
        for field_name in entries.keys():
            if not validate_single_field(field_name):
                all_valid = False
        
        empty_fields = [field_name.replace('_', ' ').title() for field_name, entry in entries.items() if not entry.get().strip()]
        
        if empty_fields:
            status_label.config(text="⚠️ Please fill in all fields!", fg=colors['warning'])
            return
        
        if not all_valid:
            status_label.config(text="⚠️ Please fix the errors before continuing.", fg=colors['warning'])
            return
            
        if not terms_var.get():
            status_label.config(text="⚠️ Please agree to the Terms of Service.", fg=colors['warning'])
            return
        
        username = entries['username'].get().strip()
        
        # Show loading
        status_label.config(text="🔄 Creating account...", fg=colors['secondary'])
        root.update()
        
        try:
            # Check if username exists
            users = read_json(USER_FILE)
            if any(u['username'] == username for u in users):
                status_label.config(text="❌ Username already exists!", fg=colors['danger'])
                return
            
            # Check if email exists
            email = entries['email'].get().strip()
            if any(u.get('email') == email for u in users):
                status_label.config(text="❌ An account with this email already exists!", fg=colors['danger'])
                return
                
            # Create new customer
            new_customer = Customer(
                username=username,
                password=entries['password'].get().strip(),
                email=email,
                address=entries['address'].get().strip(),
                phone_number=entries['phone'].get().strip()
            )
            
            customer_dict = new_customer.to_dict()
            customer_dict['full_name'] = entries['full_name'].get().strip()
            
            users.append(customer_dict)
            write_json(USER_FILE, users)
            
            status_label.config(text="✅ Account created successfully!", fg=colors['success'])
            root.update()
            
            messagebox.showinfo("Success!", 
                              f"Account created successfully!\n\n"
                              f"Welcome {username}!\nYou can now sign in with your credentials.")
            
            current_geometry = root.geometry()
            root.destroy()
            from gui.login_gui import login_gui
            login_gui(current_geometry)
            
        except Exception as e:
            status_label.config(text="❌ Registration failed!", fg=colors['danger'])
            print(f"Registration error: {e}")  # For debugging
    
    # Register button
    register_btn = tk.Button(card_content,
                            text="🎉 CREATE ACCOUNT",
                            font=('Segoe UI', 11, 'bold'),
                            bg=colors['success'],
                            fg='white',
                            border=0,
                            padx=25,
                            pady=8,
                            cursor='hand2',
                            relief='flat',
                            command=attempt_register)
    register_btn.pack(fill='x', pady=(15, 10))
    
    # Hover effects
    def on_register_enter(e):
        register_btn.configure(bg='#219a52')
    
    def on_register_leave(e):
        register_btn.configure(bg=colors['success'])
    
    register_btn.bind("<Enter>", on_register_enter)
    register_btn.bind("<Leave>", on_register_leave)
    
    # Login link
    divider_line = tk.Frame(card_content, bg=colors['light'], height=1)
    divider_line.pack(fill='x', pady=8)
    
    login_text = tk.Label(card_content,
                         text="Already have an account?",
                         font=('Segoe UI', 9),
                         bg=colors['white'],
                         fg=colors['text_light'])
    login_text.pack()
    
    def open_login():
        current_geometry = root.geometry()
        root.destroy()
        from gui.login_gui import login_gui
        login_gui(current_geometry)
    
    login_link = tk.Label(card_content,
                         text="Sign In Here",
                         font=('Segoe UI', 9, 'bold', 'underline'),
                         bg=colors['white'],
                         fg=colors['secondary'],
                         cursor='hand2')
    login_link.pack()
    login_link.bind("<Button-1>", lambda e: open_login())
    
    # Footer
    footer_text = tk.Label(card_content,
                          text="🔒 Your information is secure",
                          font=('Segoe UI', 8),
                          bg=colors['white'],
                          fg=colors['text_light'])
    footer_text.pack(pady=(8, 0))
    
    # Status bar
    status_frame = tk.Frame(root, bg=colors['light'], height=25)
    status_frame.pack(fill='x', side='bottom')
    status_frame.pack_propagate(False)
    
    status_bar_label = tk.Label(status_frame,
                               text="Use mouse wheel to scroll • Press Escape to go back",
                               font=('Segoe UI', 8),
                               bg=colors['light'],
                               fg=colors['text_light'])
    status_bar_label.pack(expand=True)
    
    # Mouse wheel scrolling
    def _on_mousewheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_mousewheel(event):
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_mousewheel(event):
        main_canvas.unbind_all("<MouseWheel>")
    
    main_canvas.bind('<Enter>', _bind_mousewheel)
    main_canvas.bind('<Leave>', _unbind_mousewheel)
    
    # Update scroll region
    def configure_scroll_region(event=None):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        canvas_width = main_canvas.winfo_width()
        if main_canvas.find_all():
            main_canvas.itemconfig(main_canvas.find_all()[0], width=canvas_width)
    
    main_canvas.bind('<Configure>', configure_scroll_region)
    scroll_container.bind('<Configure>', configure_scroll_region)
    
    # Keyboard shortcuts
    root.bind('<Escape>', lambda e: go_back())
    root.bind('<Return>', lambda e: attempt_register())
    
    # Focus on first entry
    root.after(100, lambda: entries['username'].focus())
    
    # Window close handler
    def on_closing():
        go_back()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    register_gui()