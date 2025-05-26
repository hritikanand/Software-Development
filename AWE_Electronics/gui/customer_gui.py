import tkinter as tk
from tkinter import messagebox, ttk

# Import all required modules with error handling
try:
    from models.catalogue import Catalogue
    from models.order import Order
    from models.invoice import Invoice
    from models.receipt import Receipt
    from utils.file_handler import read_json, write_json
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are available.")

ORDER_FILE = "data/orders.json"

def customer_gui(user, previous_geometry="1000x700"):
    root = tk.Tk()
    root.title(f"AWE Electronics - Welcome {user['username']}")
    root.geometry(previous_geometry)
    root.resizable(True, True)
    root.minsize(900, 600)
    
    # Modern color scheme
    colors = {
        'primary': '#2c3e50',
        'secondary': '#3498db', 
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#17a2b8',
        'light': '#ecf0f1',
        'white': '#ffffff',
        'dark': '#2c3e50',
        'gray': '#7f8c8d'
    }
    
    root.configure(bg=colors['light'])
    
    # Header with modern design
    header_frame = tk.Frame(root, bg=colors['primary'], height=70)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Header content
    header_content = tk.Frame(header_frame, bg=colors['primary'])
    header_content.pack(fill='both', expand=True, padx=20)
    
    # Welcome section
    welcome_frame = tk.Frame(header_content, bg=colors['primary'])
    welcome_frame.pack(side='left', fill='y', pady=12)
    
    company_label = tk.Label(welcome_frame,
                            text="AWE Electronics",
                            font=('Segoe UI', 14, 'bold'),
                            bg=colors['primary'],
                            fg='white')
    company_label.pack()
    
    welcome_label = tk.Label(welcome_frame,
                            text=f"Welcome, {user['username']}!",
                            font=('Segoe UI', 10),
                            bg=colors['primary'],
                            fg=colors['light'])
    welcome_label.pack()
    
    # Header controls
    header_controls = tk.Frame(header_content, bg=colors['primary'])
    header_controls.pack(side='right', fill='y', pady=12)
    
    # Cart info with dynamic update
    def update_cart_display():
        cart_count = len(user.get('cart', []))
        cart_btn.config(text=f"🛒 Cart ({cart_count})")
    
    cart_btn = tk.Button(header_controls,
                        text=f"🛒 Cart ({len(user.get('cart', []))})",
                        font=('Segoe UI', 10, 'bold'),
                        bg=colors['success'],
                        fg='white',
                        border=0,
                        padx=15,
                        pady=6,
                        cursor='hand2',
                        relief='flat',
                        command=lambda: notebook.select(1))
    cart_btn.pack(side='left', padx=(0, 8))
    
    # Navigation buttons
    def go_home():
        if messagebox.askyesno("Go Home", "Return to main menu?"):
            current_geometry = root.geometry()
            root.destroy()
            from gui.start_gui import start_gui
            start_gui()
            
    home_btn = tk.Button(header_controls,
                        text="🏠 Home",
                        font=('Segoe UI', 10, 'bold'),
                        bg=colors['secondary'],
                        fg='white',
                        border=0,
                        padx=15,
                        pady=6,
                        cursor='hand2',
                        relief='flat',
                        command=go_home)
    home_btn.pack(side='left', padx=(0, 8))
    
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            current_geometry = root.geometry()
            root.destroy()
            from gui.start_gui import start_gui
            start_gui()
    
    logout_btn = tk.Button(header_controls,
                          text="🚪 Logout",
                          font=('Segoe UI', 10, 'bold'),
                          bg=colors['danger'],
                          fg='white',
                          border=0,
                          padx=15,
                          pady=6,
                          cursor='hand2',
                          relief='flat',
                          command=logout)
    logout_btn.pack(side='left')
    
    # Main content with modern notebook
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Customer.TNotebook', background=colors['light'])
    style.configure('Customer.TNotebook.Tab', 
                   padding=[18, 8], 
                   font=('Segoe UI', 10, 'bold'))
    
    notebook = ttk.Notebook(root, style='Customer.TNotebook')
    notebook.pack(fill='both', expand=True, padx=12, pady=12)
    
    # Store cart loading function for tab switching
    cart_load_function = None
    
    # Create all tabs
    create_products_tab(notebook, colors, user, update_cart_display)
    cart_load_function = create_cart_tab(notebook, colors, user, update_cart_display)
    create_orders_tab(notebook, colors, user)
    
    # Handle tab changes to refresh cart when cart tab is selected
    def on_tab_change(event):
        selected_tab = event.widget.tab('current')['text']
        if '🛒' in selected_tab and cart_load_function:
            # When cart tab is selected, refresh the cart display
            root.after(10, cart_load_function)  # Small delay to ensure tab is fully loaded
    
    notebook.bind('<<NotebookTabChanged>>', on_tab_change)
    
    # Initialize cart display
    update_cart_display()
    
    # Window close handler
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit AWE Electronics?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

def create_products_tab(notebook, colors, user, update_cart_display):
    """Create the products browsing tab"""
    products_frame = tk.Frame(notebook, bg='white')
    notebook.add(products_frame, text="🛍️ Browse Products")
    
    # Search section
    search_section = tk.Frame(products_frame, bg='white', relief='solid', bd=1)
    search_section.pack(fill='x', padx=15, pady=15)
    
    search_title = tk.Label(search_section, 
                           text="Find Your Perfect Product", 
                           font=('Segoe UI', 14, 'bold'), 
                           bg='white', 
                           fg=colors['primary'])
    search_title.pack(pady=12)
    
    search_controls = tk.Frame(search_section, bg='white')
    search_controls.pack(fill='x', padx=20, pady=(0, 15))
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_controls, 
                           textvariable=search_var,
                           font=('Segoe UI', 11), 
                           relief='solid', 
                           bd=2,
                           width=40)
    search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=6)
    
    def search_products():
        search_term = search_var.get().strip().lower()
        load_products(search_term)
    
    search_btn = tk.Button(search_controls, 
                          text="🔍 Search", 
                          font=('Segoe UI', 10, 'bold'),
                          bg=colors['secondary'], 
                          fg='white',
                          border=0, 
                          padx=20, 
                          pady=8, 
                          cursor='hand2',
                          relief='flat',
                          command=search_products)
    search_btn.pack(side='right')
    
    search_entry.bind('<Return>', lambda e: search_products())
    search_entry.bind('<KeyRelease>', lambda e: search_products())
    
    # Products display
    products_container = tk.Frame(products_frame, bg='white')
    products_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    products_title = tk.Label(products_container, 
                             text="Available Products", 
                             font=('Segoe UI', 12, 'bold'), 
                             bg='white', 
                             fg=colors['primary'])
    products_title.pack(anchor='w', pady=(0, 8))
    
    # Products listbox
    products_list_frame = tk.Frame(products_container, bg='white', relief='solid', bd=1)
    products_list_frame.pack(fill='both', expand=True)
    
    products_listbox = tk.Listbox(products_list_frame, 
                                 font=('Segoe UI', 9),
                                 selectbackground=colors['secondary'],
                                 selectforeground='white',
                                 bg='white',
                                 relief='flat')
    products_scrollbar = tk.Scrollbar(products_list_frame, orient='vertical', 
                                     command=products_listbox.yview)
    products_listbox.configure(yscrollcommand=products_scrollbar.set)
    
    products_listbox.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    products_scrollbar.pack(side='right', fill='y')
    
    def load_products(search_term=""):
        try:
            products_listbox.delete(0, tk.END)
            cat = Catalogue()
            
            for product in cat.list_all_products():
                if (not search_term or 
                    search_term in product.name.lower() or 
                    search_term in product.category.lower() or
                    search_term in product.product_id.lower()):
                    
                    stock_status = "✅ In Stock" if product.stock > 5 else "⚠️ Low Stock" if product.stock > 0 else "❌ Out of Stock"
                    display_text = f"{product.product_id} | {product.name} | ${product.price:.2f} | {product.category} | {stock_status} ({product.stock})"
                    products_listbox.insert(tk.END, display_text)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
    
    # Add to cart section
    cart_section = tk.Frame(products_frame, bg=colors['light'], relief='solid', bd=1)
    cart_section.pack(fill='x', padx=15, pady=(0, 15))
    
    cart_section_title = tk.Label(cart_section, 
                                 text="Add to Cart", 
                                 font=('Segoe UI', 12, 'bold'), 
                                 bg=colors['light'], 
                                 fg=colors['primary'])
    cart_section_title.pack(pady=12)
    
    cart_controls = tk.Frame(cart_section, bg=colors['light'])
    cart_controls.pack(fill='x', padx=20, pady=(0, 15))
    
    # Product ID selection
    pid_frame = tk.Frame(cart_controls, bg=colors['light'])
    pid_frame.pack(side='left', padx=(0, 15))
    
    tk.Label(pid_frame, text="Product ID:", 
            font=('Segoe UI', 9, 'bold'), bg=colors['light']).pack()
    product_id_entry = tk.Entry(pid_frame, font=('Segoe UI', 10), 
                               width=12, relief='solid', bd=2)
    product_id_entry.pack(ipady=4)
    
    # Quantity selection
    qty_frame = tk.Frame(cart_controls, bg=colors['light'])
    qty_frame.pack(side='left', padx=(0, 15))
    
    tk.Label(qty_frame, text="Quantity:", 
            font=('Segoe UI', 9, 'bold'), bg=colors['light']).pack()
    quantity_entry = tk.Entry(qty_frame, font=('Segoe UI', 10), 
                             width=8, relief='solid', bd=2)
    quantity_entry.pack(ipady=4)
    quantity_entry.insert(0, "1")
    
    # Auto-fill product ID when selecting
    def on_product_select(event):
        selection = products_listbox.curselection()
        if selection:
            selected_text = products_listbox.get(selection[0])
            product_id = selected_text.split(' | ')[0]
            product_id_entry.delete(0, tk.END)
            product_id_entry.insert(0, product_id)
    
    products_listbox.bind('<<ListboxSelect>>', on_product_select)
    
    def add_to_cart():
        product_id = product_id_entry.get().strip()
        
        try:
            quantity = int(quantity_entry.get().strip())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid quantity!")
            return
            
        if not product_id:
            messagebox.showerror("Missing Information", "Please enter a product ID!")
            return
            
        try:
            cat = Catalogue()
            product = None
            
            # Find product by ID
            for p in cat.list_all_products():
                if p.product_id == product_id:
                    product = p
                    break
            
            if not product:
                messagebox.showerror("Product Not Found", f"Product ID '{product_id}' not found!")
                return
                
            if product.stock < quantity:
                messagebox.showerror("Insufficient Stock", 
                                   f"Only {product.stock} items available!")
                return
            
            # Initialize cart if it doesn't exist
            if 'cart' not in user:
                user['cart'] = []
            
            # Check if product already in cart
            existing_item = None
            for item in user["cart"]:
                if item["product_id"] == product_id:
                    existing_item = item
                    break
            
            if existing_item:
                existing_item["quantity"] += quantity
                messagebox.showinfo("Cart Updated", 
                                  f"Updated quantity for {product.name}")
            else:
                user["cart"].append({"product_id": product_id, "quantity": quantity})
                messagebox.showinfo("Added to Cart", 
                                  f"Added {quantity} x {product.name} to cart!")
            
            # Update cart display and clear entries
            update_cart_display()
            product_id_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, "1")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to cart: {str(e)}")
    
    add_cart_btn = tk.Button(cart_controls, 
                            text="🛒 Add to Cart", 
                            font=('Segoe UI', 10, 'bold'), 
                            bg=colors['success'], 
                            fg='white',
                            border=0, 
                            padx=20, 
                            pady=8, 
                            cursor='hand2',
                            relief='flat',
                            command=add_to_cart)
    add_cart_btn.pack(side='left')
    
    # Load initial products
    load_products()
    
    # Focus on search
    search_entry.focus()

def create_cart_tab(notebook, colors, user, update_cart_display):
    """Create the shopping cart tab - returns load_cart function for tab switching"""
    cart_frame = tk.Frame(notebook, bg='white')
    notebook.add(cart_frame, text="🛒 Shopping Cart")
    
    cart_header = tk.Frame(cart_frame, bg='white')
    cart_header.pack(fill='x', padx=20, pady=15)
    
    cart_title = tk.Label(cart_header, 
                         text="Your Shopping Cart", 
                         font=('Segoe UI', 16, 'bold'), 
                         bg='white', 
                         fg=colors['primary'])
    cart_title.pack()
    
    # Cart display
    cart_display_frame = tk.Frame(cart_frame, bg='white', relief='solid', bd=1)
    cart_display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    cart_listbox = tk.Listbox(cart_display_frame, 
                             font=('Segoe UI', 10),
                             selectbackground=colors['secondary'],
                             selectforeground='white',
                             bg='white',
                             relief='flat',
                             height=10)
    cart_scrollbar = tk.Scrollbar(cart_display_frame, orient='vertical', 
                                 command=cart_listbox.yview)
    cart_listbox.configure(yscrollcommand=cart_scrollbar.set)
    
    cart_listbox.pack(side='left', fill='both', expand=True, padx=15, pady=15)
    cart_scrollbar.pack(side='right', fill='y')
    
    # Cart summary and actions
    cart_bottom_frame = tk.Frame(cart_frame, bg='white')
    cart_bottom_frame.pack(fill='x', padx=20, pady=(0, 20))
    
    total_label = tk.Label(cart_bottom_frame, 
                          text="Total: $0.00", 
                          font=('Segoe UI', 14, 'bold'), 
                          bg='white', 
                          fg=colors['success'])
    total_label.pack(anchor='e', pady=(0, 10))
    
    def load_cart():
        try:
            cart_listbox.delete(0, tk.END)
            
            # Initialize cart if it doesn't exist
            if 'cart' not in user:
                user['cart'] = []
            
            # Load products using both methods for reliability
            products_dict = {}
            
            # Method 1: Try Catalogue class
            try:
                cat = Catalogue()
                for product in cat.products:
                    products_dict[product.product_id] = product
            except Exception as cat_error:
                print(f"Catalogue loading failed: {cat_error}")
                # Method 2: Try direct JSON loading
                try:
                    products_data = read_json("data/products.json")
                    for prod_dict in products_data:
                        class SimpleProduct:
                            def __init__(self, data):
                                self.product_id = data['product_id']
                                self.name = data['name']
                                self.price = data['price']
                                self.category = data.get('category', '')
                                self.stock = data.get('stock', 0)
                        
                        products_dict[prod_dict['product_id']] = SimpleProduct(prod_dict)
                except Exception as json_error:
                    print(f"Direct JSON loading failed: {json_error}")
            
            total = 0
            
            if not user.get("cart"):
                cart_listbox.insert(tk.END, "Your cart is empty. Start shopping!")
                total_label.config(text="Total: $0.00")
                update_cart_display()
                return
            
            for cart_item in user.get("cart", []):
                product_id = cart_item["product_id"]
                quantity = cart_item["quantity"]
                
                if product_id in products_dict:
                    product = products_dict[product_id]
                    subtotal = product.price * quantity
                    total += subtotal
                    
                    display_text = f"{product.name} | Qty: {quantity} | ${product.price:.2f} each | Subtotal: ${subtotal:.2f}"
                    cart_listbox.insert(tk.END, display_text)
                else:
                    # Product not found, show error but keep cart item
                    display_text = f"Product {product_id} | Qty: {quantity} | Product not found!"
                    cart_listbox.insert(tk.END, display_text)
                    
            total_label.config(text=f"Total: ${total:.2f}")
            update_cart_display()
            
        except Exception as e:
            error_msg = f"Failed to load cart: {str(e)}"
            cart_listbox.delete(0, tk.END)
            cart_listbox.insert(tk.END, f"Error: {error_msg}")
            print(f"Cart loading error: {e}")
            import traceback
            traceback.print_exc()
    
    def remove_from_cart():
        selection = cart_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove!")
            return
        
        if not user.get("cart"):
            messagebox.showinfo("Empty Cart", "Your cart is already empty!")
            return
            
        if messagebox.askyesno("Remove Item", "Remove this item from cart?"):
            try:
                # Remove item at selected index
                index = selection[0]
                if index < len(user["cart"]):
                    removed_item = user["cart"].pop(index)
                    load_cart()
                    messagebox.showinfo("Item Removed", "Item removed from cart!")
                else:
                    messagebox.showerror("Error", "Invalid selection!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove item: {str(e)}")
    
    def clear_cart():
        if not user.get("cart"):
            messagebox.showinfo("Empty Cart", "Your cart is already empty!")
            return
            
        if messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            try:
                user["cart"] = []
                load_cart()  # This will refresh the display
                messagebox.showinfo("Cart Cleared", "All items removed from cart!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear cart: {str(e)}")
    
    # Cart action buttons
    cart_actions = tk.Frame(cart_bottom_frame, bg='white')
    cart_actions.pack(anchor='e')
    
    remove_btn = tk.Button(cart_actions, 
                          text="🗑️ Remove Selected", 
                          font=('Segoe UI', 10, 'bold'), 
                          bg=colors['warning'], 
                          fg='white',
                          border=0, 
                          padx=15, 
                          pady=8, 
                          cursor='hand2',
                          relief='flat',
                          command=remove_from_cart)
    remove_btn.pack(side='left', padx=(0, 8))
    
    clear_cart_btn = tk.Button(cart_actions, 
                              text="🗑️ Clear Cart", 
                              font=('Segoe UI', 10, 'bold'), 
                              bg=colors['danger'], 
                              fg='white',
                              border=0, 
                              padx=15, 
                              pady=8, 
                              cursor='hand2',
                              relief='flat',
                              command=clear_cart)
    clear_cart_btn.pack(side='left', padx=(0, 10))
    
    def checkout():
        if not user.get("cart"):
            messagebox.showerror("Empty Cart", "Your cart is empty!")
            return
        
        # Create checkout window
        CheckoutWindow(cart_frame, user, colors, load_cart)
    
    checkout_btn = tk.Button(cart_actions, 
                           text="💳 Checkout", 
                           font=('Segoe UI', 11, 'bold'), 
                           bg=colors['success'], 
                           fg='white',
                           border=0, 
                           padx=20, 
                           pady=10, 
                           cursor='hand2',
                           relief='flat',
                           command=checkout)
    checkout_btn.pack(side='left')
    
    # Don't load cart initially - let tab switching handle it
    # Return the load_cart function so main can call it on tab change
    return load_cart

def create_orders_tab(notebook, colors, user):
    """Create the order history tab"""
    orders_frame = tk.Frame(notebook, bg='white')
    notebook.add(orders_frame, text="📋 Order History")
    
    orders_header = tk.Frame(orders_frame, bg='white')
    orders_header.pack(fill='x', padx=20, pady=15)
    
    orders_title = tk.Label(orders_header, 
                           text="Your Order History", 
                           font=('Segoe UI', 16, 'bold'), 
                           bg='white', 
                           fg=colors['primary'])
    orders_title.pack()
    
    orders_listbox = tk.Listbox(orders_frame, 
                               font=('Segoe UI', 10),
                               selectbackground=colors['secondary'],
                               selectforeground='white',
                               bg='white',
                               relief='solid',
                               bd=1)
    orders_listbox.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def load_orders():
        try:
            orders_listbox.delete(0, tk.END)
            orders = read_json(ORDER_FILE)
            user_orders = [order for order in orders 
                          if order["order"]["user_id"] == user["username"]]
            
            if not user_orders:
                orders_listbox.insert(tk.END, "No orders found. Start shopping!")
                return
            
            for order_data in user_orders:
                order = order_data["order"]
                order_id = order["order_id"][:8] + "..."
                items_count = len(order["items"])
                total = f"${order['total']:.2f}"
                
                display_text = f"Order {order_id} | {items_count} items | {total} | ✅ Completed"
                orders_listbox.insert(tk.END, display_text)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {str(e)}")
    
    # Load orders
    load_orders()

class CheckoutWindow:
    """Modern checkout window with proper sizing"""
    def __init__(self, parent, user, colors, refresh_cart_callback):
        self.user = user
        self.colors = colors
        self.refresh_cart = refresh_cart_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Checkout - AWE Electronics")
        
        # Start with a reasonable size
        self.window.geometry("500x700")
        self.window.configure(bg='white')
        self.window.transient(parent)
        self.window.resizable(True, True)
        self.window.grab_set()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (250)
        y = (self.window.winfo_screenheight() // 2) - (350)
        self.window.geometry(f"500x700+{x}+{y}")
        
        self.create_widgets()
        
        # Auto-resize to fit content after creation
        self.window.after(100, self.auto_resize)
    
    def auto_resize(self):
        """Auto-resize window to fit content"""
        try:
            self.window.update_idletasks()
            
            # Get the required size
            req_width = self.window.winfo_reqwidth()
            req_height = self.window.winfo_reqheight()
            
            # Add some padding
            width = max(500, req_width + 50)
            height = max(600, min(800, req_height + 100))  # Cap at 800px height
            
            # Update geometry
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            print(f"DEBUG: Auto-resize error: {e}")
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, 
                text="Complete Your Order", 
                font=('Segoe UI', 16, 'bold'), 
                bg=self.colors['primary'], 
                fg='white').pack(expand=True)
        
        # Create main frame with scrolling capability
        main_frame = tk.Frame(self.window, bg='white')
        main_frame.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Content inside scrollable frame
        content = tk.Frame(scrollable_frame, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Shipping form
        shipping_frame = tk.LabelFrame(content, 
                                      text="📦 Shipping Information", 
                                      font=('Segoe UI', 11, 'bold'), 
                                      bg='white',
                                      fg=self.colors['primary'])
        shipping_frame.pack(fill='x', pady=(0, 15))
        
        self.entries = {}
        fields = ["Full Name", "Address", "Phone Number"]
        
        for field in fields:
            tk.Label(shipping_frame, 
                    text=f"{field}:", 
                    font=('Segoe UI', 10), 
                    bg='white').pack(anchor='w', padx=10, pady=(8, 2))
            entry = tk.Entry(shipping_frame, 
                           font=('Segoe UI', 10), 
                           relief='solid', 
                           bd=2)
            entry.pack(fill='x', padx=10, pady=(0, 8), ipady=5)
            self.entries[field] = entry
        
        # Payment method
        payment_frame = tk.LabelFrame(content, 
                                     text="💳 Payment Method", 
                                     font=('Segoe UI', 11, 'bold'), 
                                     bg='white',
                                     fg=self.colors['primary'])
        payment_frame.pack(fill='x', pady=(0, 15))
        
        self.payment_var = tk.StringVar(value="PayPal")
        
        payment_options = [
            ("💳 Credit Card", "Credit Card"),
            ("🅿️ PayPal", "PayPal")
        ]
        
        for text, value in payment_options:
            tk.Radiobutton(payment_frame, 
                          text=text, 
                          variable=self.payment_var, 
                          value=value, 
                          font=('Segoe UI', 10), 
                          bg='white').pack(anchor='w', padx=10, pady=2)
        
        tk.Label(payment_frame, 
                text="Account/Cardholder Name:", 
                font=('Segoe UI', 10), 
                bg='white').pack(anchor='w', padx=10, pady=(8, 2))
        self.payment_name_entry = tk.Entry(payment_frame, 
                                          font=('Segoe UI', 10), 
                                          relief='solid', 
                                          bd=2)
        self.payment_name_entry.pack(fill='x', padx=10, pady=(0, 8), ipady=5)
        
        # Order summary
        summary_frame = tk.LabelFrame(content, 
                                     text="📋 Order Summary", 
                                     font=('Segoe UI', 11, 'bold'), 
                                     bg='white',
                                     fg=self.colors['primary'])
        summary_frame.pack(fill='x', pady=(0, 15))
        
        # Calculate total using the same method as cart display
        total = 0
        try:
            # Load products using both methods for reliability
            products_dict = {}
            
            # Method 1: Catalogue
            try:
                cat = Catalogue()
                for product in cat.products:
                    products_dict[product.product_id] = product
            except Exception as cat_error:
                print(f"Catalogue loading failed: {cat_error}")
                # Method 2: Direct JSON
                try:
                    products_data = read_json("data/products.json")
                    for prod_dict in products_data:
                        class SimpleProduct:
                            def __init__(self, data):
                                self.product_id = data['product_id']
                                self.name = data['name']
                                self.price = data['price']
                        products_dict[prod_dict['product_id']] = SimpleProduct(prod_dict)
                except Exception as json_error:
                    print(f"Direct JSON loading failed: {json_error}")
            
            for cart_item in self.user.get("cart", []):
                product_id = cart_item["product_id"]
                if product_id in products_dict:
                    product = products_dict[product_id]
                    total += product.price * cart_item["quantity"]
        except Exception as e:
            print(f"Checkout total calculation error: {e}")
        
        tk.Label(summary_frame, 
                text=f"Total Amount: ${total:.2f}", 
                font=('Segoe UI', 14, 'bold'), 
                bg='white', 
                fg=self.colors['success']).pack(padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(content, bg='white')
        buttons_frame.pack(fill='x', pady=15)
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, 
                              text="❌ Cancel", 
                              font=('Segoe UI', 11, 'bold'), 
                              bg=self.colors['danger'], 
                              fg='white',
                              border=0, 
                              padx=20, 
                              pady=10, 
                              cursor='hand2',
                              relief='flat',
                              command=self.window.destroy)
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Place order button
        place_order_btn = tk.Button(buttons_frame, 
                                   text="🎉 Place Order", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   bg=self.colors['success'], 
                                   fg='white',
                                   border=0, 
                                   padx=30, 
                                   pady=12, 
                                   cursor='hand2',
                                   relief='flat',
                                   command=self.place_order)
        place_order_btn.pack(side='right')
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
    
    def place_order(self):
        # Validate inputs
        if not all(entry.get().strip() for entry in self.entries.values()):
            messagebox.showerror("Missing Information", 
                               "Please fill in all shipping details!")
            return
            
        if not self.payment_name_entry.get().strip():
            messagebox.showerror("Missing Information", 
                               "Please enter payment name!")
            return
        
        try:
            # Create order
            shipping = {
                "name": self.entries["Full Name"].get().strip(),
                "address": self.entries["Address"].get().strip(),
                "phone": self.entries["Phone Number"].get().strip()
            }
            
            payment_method = f"{self.payment_var.get()} - {self.payment_name_entry.get().strip()}"
            
            items = []
            
            # Use same product lookup method as cart display
            products_dict = {}
            try:
                cat = Catalogue()
                for product in cat.products:
                    products_dict[product.product_id] = product
            except Exception as cat_error:
                print(f"Catalogue loading failed: {cat_error}")
                try:
                    products_data = read_json("data/products.json")
                    for prod_dict in products_data:
                        class SimpleProduct:
                            def __init__(self, data):
                                self.product_id = data['product_id']
                                self.name = data['name']
                                self.price = data['price']
                        products_dict[prod_dict['product_id']] = SimpleProduct(prod_dict)
                except Exception as json_error:
                    print(f"JSON loading failed: {json_error}")
                    messagebox.showerror("Error", "Failed to load product information!")
                    return
            
            for cart_item in self.user["cart"]:
                product_id = cart_item["product_id"]
                if product_id in products_dict:
                    product = products_dict[product_id]
                    items.append({
                        "product_id": product.product_id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": cart_item["quantity"]
                    })
            
            if not items:
                messagebox.showerror("Error", "No valid items in cart!")
                return
            
            order = Order(self.user["username"], items, shipping, payment_method)
            invoice = Invoice(order)
            receipt = Receipt(invoice, payment_method)
            
            # Save order
            try:
                orders = read_json(ORDER_FILE)
                orders.append({
                    "order": order.to_dict(),
                    "invoice": invoice.to_dict(),
                    "receipt": receipt.to_dict()
                })
                write_json(ORDER_FILE, orders)
            except Exception as save_error:
                print(f"Order save error: {save_error}")
                messagebox.showerror("Error", f"Failed to save order: {save_error}")
                return
            
            # Clear cart
            self.user["cart"] = []
            self.refresh_cart()
            
            self.window.destroy()
            
            # Success message
            success_msg = (f"🎉 Order placed successfully!\n\n"
                         f"Order ID: {order.order_id[:8]}...\n"
                         f"Total: ${invoice.amount:.2f}\n"
                         f"Receipt ID: {receipt.receipt_id[:8]}...\n\n"
                         f"Thank you for shopping with AWE Electronics!")
            
            messagebox.showinfo("Order Confirmed", success_msg)
            
        except Exception as e:
            messagebox.showerror("Order Failed", f"Failed to place order: {str(e)}")
            print(f"Order placement error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Test with dummy user
    test_user = {
        "username": "test",
        "role": "customer",
        "cart": []
    }
    customer_gui(test_user)