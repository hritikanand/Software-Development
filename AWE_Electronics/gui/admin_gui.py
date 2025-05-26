import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from utils.file_handler import read_json, write_json

PRODUCT_FILE = "data/products.json"
ORDER_FILE = "data/orders.json"

def admin_gui(previous_geometry="1000x700"):
    root = tk.Tk()
    root.title("AWE Electronics - Admin Dashboard")
    root.geometry(previous_geometry)
    root.resizable(True, True)
    root.minsize(1000, 700)
    
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
    
    # Header with enhanced design - Fixed layout
    header_frame = tk.Frame(root, bg=colors['primary'], height=80)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    
    # Header content - properly packed
    header_content = tk.Frame(header_frame, bg=colors['primary'])
    header_content.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Left side - Admin title and stats
    header_left = tk.Frame(header_content, bg=colors['primary'])
    header_left.pack(side='left', fill='y')
    
    admin_label = tk.Label(header_left,
                          text="Admin Dashboard",
                          font=('Segoe UI', 18, 'bold'),
                          bg=colors['primary'],
                          fg='white')
    admin_label.pack(anchor='w')
    
    # System stats
    try:
        products = read_json(PRODUCT_FILE)
        orders = read_json(ORDER_FILE)
        
        stats_text = f"📦 {len(products)} Products | 📋 {len(orders)} Orders"
        stats_label = tk.Label(header_left,
                              text=stats_text,
                              font=('Segoe UI', 10),
                              bg=colors['success'],
                              fg='white',
                              padx=10,
                              pady=3)
        stats_label.pack(anchor='w', pady=(5, 0))
    except:
        stats_label = tk.Label(header_left,
                              text="📊 System Ready",
                              font=('Segoe UI', 10),
                              bg=colors['info'],
                              fg='white',
                              padx=10,
                              pady=3)
        stats_label.pack(anchor='w', pady=(5, 0))
    
    # Right side - Navigation buttons
    header_right = tk.Frame(header_content, bg=colors['primary'])
    header_right.pack(side='right', fill='y')
    
    # Navigation buttons
    def go_home():
        if messagebox.askyesno("Go Home", "Return to main menu?"):
            current_geometry = root.geometry()
            root.destroy()
            from gui.start_gui import start_gui
            start_gui()
    
    home_btn = tk.Button(header_right,
                        text="🏠 Home",
                        font=('Segoe UI', 10, 'bold'),
                        bg=colors['secondary'],
                        fg='white',
                        border=0,
                        padx=15,
                        pady=8,
                        cursor='hand2',
                        relief='flat',
                        command=go_home)
    home_btn.pack(side='right', padx=(10, 0))
    
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            current_geometry = root.geometry()
            root.destroy()
            from gui.start_gui import start_gui
            start_gui()
    
    logout_btn = tk.Button(header_right,
                          text="🚪 Logout",
                          font=('Segoe UI', 10, 'bold'),
                          bg=colors['danger'],
                          fg='white',
                          border=0,
                          padx=15,
                          pady=8,
                          cursor='hand2',
                          relief='flat',
                          command=logout)
    logout_btn.pack(side='right')
    
    # Main content with enhanced notebook
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Admin.TNotebook', background=colors['light'])
    style.configure('Admin.TNotebook.Tab', 
                   padding=[20, 10], 
                   font=('Segoe UI', 10, 'bold'))
    
    notebook = ttk.Notebook(root, style='Admin.TNotebook')
    notebook.pack(fill='both', expand=True, padx=15, pady=15)
    
    # Create all tabs
    create_dashboard_tab(notebook, colors)
    create_products_tab(notebook, colors, root)
    create_orders_tab(notebook, colors)
    create_reports_tab(notebook, colors)
    
    # Window close handler
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the admin panel?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

def create_dashboard_tab(notebook, colors):
    """Create the dashboard tab"""
    dashboard_frame = tk.Frame(notebook, bg=colors['white'])
    notebook.add(dashboard_frame, text="📊 Dashboard")
    
    # Dashboard header
    dash_header = tk.Frame(dashboard_frame, bg=colors['white'])
    dash_header.pack(fill='x', padx=20, pady=15)
    
    dash_title = tk.Label(dash_header,
                         text="Business Overview",
                         font=('Segoe UI', 16, 'bold'),
                         bg=colors['white'],
                         fg=colors['primary'])
    dash_title.pack()
    
    # Stats container
    stats_container = tk.Frame(dashboard_frame, bg=colors['white'])
    stats_container.pack(fill='x', padx=20, pady=10)
    
    try:
        products = read_json(PRODUCT_FILE)
        orders = read_json(ORDER_FILE)
        
        # Calculate statistics
        total_products = len(products)
        low_stock_count = len([p for p in products if p.get('stock', 0) < 5])
        out_of_stock = len([p for p in products if p.get('stock', 0) == 0])
        total_orders = len(orders)
        total_revenue = sum(order.get('order', {}).get('total', 0) for order in orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        stats_data = [
            ("Total Products", total_products, colors['secondary'], "📦"),
            ("Low Stock Items", low_stock_count, colors['warning'], "⚠️"),
            ("Out of Stock", out_of_stock, colors['danger'], "❌"),
            ("Total Orders", total_orders, colors['success'], "📋"),
            ("Total Revenue", f"${total_revenue:.2f}", colors['info'], "💰"),
            ("Avg Order Value", f"${avg_order_value:.2f}", colors['primary'], "📊")
        ]
        
        # Create stats grid
        stats_grid = tk.Frame(stats_container, bg=colors['white'])
        stats_grid.pack(fill='x')
        
        for i, (title, value, color, icon) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            card = tk.Frame(stats_grid, bg=colors['light'], relief='solid', bd=1, padx=20, pady=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            stats_grid.columnconfigure(col, weight=1)
            
            # Icon
            icon_label = tk.Label(card, text=icon, font=('Segoe UI', 20), 
                                 bg=colors['light'], fg=color)
            icon_label.pack()
            
            # Value
            value_label = tk.Label(card, text=str(value), font=('Segoe UI', 14, 'bold'), 
                                  bg=colors['light'], fg=color)
            value_label.pack(pady=(5, 0))
            
            # Title
            title_label = tk.Label(card, text=title, font=('Segoe UI', 10), 
                                  bg=colors['light'], fg=colors['gray'])
            title_label.pack()
            
    except Exception as e:
        error_label = tk.Label(stats_container, 
                              text=f"⚠️ Error loading dashboard data:\n{str(e)}", 
                              font=('Segoe UI', 12), 
                              bg=colors['white'], 
                              fg=colors['danger'],
                              justify='center')
        error_label.pack(expand=True)
    
    # Quick actions section
    actions_frame = tk.Frame(dashboard_frame, bg=colors['white'])
    actions_frame.pack(fill='x', padx=20, pady=20)
    
    actions_title = tk.Label(actions_frame,
                            text="Quick Actions",
                            font=('Segoe UI', 14, 'bold'),
                            bg=colors['white'],
                            fg=colors['primary'])
    actions_title.pack(anchor='w', pady=(0, 10))
    
    actions_container = tk.Frame(actions_frame, bg=colors['white'])
    actions_container.pack(fill='x')
    
    def quick_add_product():
        notebook.select(1)  # Switch to products tab
    
    def quick_view_orders():
        notebook.select(2)  # Switch to orders tab
    
    def quick_generate_report():
        notebook.select(3)  # Switch to reports tab
    
    actions = [
        ("📦 Add Product", quick_add_product, colors['success']),
        ("📋 View Orders", quick_view_orders, colors['secondary']),
        ("📊 Generate Report", quick_generate_report, colors['info'])
    ]
    
    for i, (text, command, color) in enumerate(actions):
        btn = tk.Button(actions_container,
                       text=text,
                       font=('Segoe UI', 11, 'bold'),
                       bg=color,
                       fg='white',
                       border=0,
                       padx=20,
                       pady=10,
                       cursor='hand2',
                       relief='flat',
                       command=command)
        btn.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
        actions_container.columnconfigure(i, weight=1)

def create_products_tab(notebook, colors, root):
    """Create the products management tab"""
    products_frame = tk.Frame(notebook, bg=colors['white'])
    notebook.add(products_frame, text="📦 Products")
    
    # Product header
    product_header = tk.Frame(products_frame, bg=colors['white'])
    product_header.pack(fill='x', padx=20, pady=15)
    
    product_title = tk.Label(product_header,
                            text="Product Management",
                            font=('Segoe UI', 16, 'bold'),
                            bg=colors['white'],
                            fg=colors['primary'])
    product_title.pack(side='left')
    
    # Toolbar
    toolbar_frame = tk.Frame(product_header, bg=colors['white'])
    toolbar_frame.pack(side='right')
    
    # Product functions
    def add_product():
        dialog = ProductDialog(root, "Add New Product")
        if dialog.result:
            try:
                products = read_json(PRODUCT_FILE)
                
                if any(p['product_id'] == dialog.result['product_id'] for p in products):
                    messagebox.showerror("Product Exists", 
                                       "Product ID already exists! Please use a different ID.")
                    return
                    
                products.append(dialog.result)
                write_json(PRODUCT_FILE, products)
                load_products()
                messagebox.showinfo("Success", 
                                  f"Product '{dialog.result['name']}' added successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product:\n{str(e)}")
    
    def edit_product():
        selection = products_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to edit!")
            return
            
        selected_text = products_listbox.get(selection[0])
        product_id = selected_text.split(']')[0][1:]
        
        try:
            products = read_json(PRODUCT_FILE)
            product_data = next((p for p in products if p['product_id'] == product_id), None)
            
            if product_data:
                dialog = ProductDialog(root, "Edit Product", product_data)
                if dialog.result:
                    # Update the product
                    for i, p in enumerate(products):
                        if p['product_id'] == product_id:
                            products[i] = dialog.result
                            break
                    
                    write_json(PRODUCT_FILE, products)
                    load_products()
                    messagebox.showinfo("Success", "Product updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit product:\n{str(e)}")
    
    def update_stock():
        selection = products_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a product to update stock!")
            return
            
        selected_text = products_listbox.get(selection[0])
        product_id = selected_text.split(']')[0][1:]
        
        try:
            products = read_json(PRODUCT_FILE)
            current_stock = 0
            for product in products:
                if product['product_id'] == product_id:
                    current_stock = product.get('stock', 0)
                    break
            
            new_stock = simpledialog.askinteger("Update Stock", 
                                               f"Product: {product_id}\n"
                                               f"Current Stock: {current_stock}\n\n"
                                               f"Enter new stock quantity:", 
                                               minvalue=0,
                                               initialvalue=current_stock)
            
            if new_stock is not None:
                for product in products:
                    if product['product_id'] == product_id:
                        old_stock = product.get('stock', 0)
                        product['stock'] = new_stock
                        break
                        
                write_json(PRODUCT_FILE, products)
                load_products()
                messagebox.showinfo("Stock Updated", 
                                  f"Stock updated from {old_stock} to {new_stock}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update stock:\n{str(e)}")
    
    def delete_product():
        selection = products_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a product to delete!")
            return
            
        selected_text = products_listbox.get(selection[0])
        product_id = selected_text.split(']')[0][1:]
        
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete product {product_id}?\n\n"
                             "This action cannot be undone!"):
            try:
                products = read_json(PRODUCT_FILE)
                original_count = len(products)
                products = [p for p in products if p['product_id'] != product_id]
                
                if len(products) < original_count:
                    write_json(PRODUCT_FILE, products)
                    load_products()
                    messagebox.showinfo("Success", f"Product {product_id} deleted successfully!")
                else:
                    messagebox.showwarning("Not Found", "Product not found!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product:\n{str(e)}")
    
    # Toolbar buttons
    toolbar_buttons = [
        ("➕ Add", add_product, colors['success']),
        ("✏️ Edit", edit_product, colors['secondary']),
        ("🔄 Update Stock", update_stock, colors['warning']),
        ("🗑️ Delete", delete_product, colors['danger'])
    ]
    
    for text, command, color in toolbar_buttons:
        btn = tk.Button(toolbar_frame, 
                       text=text, 
                       font=('Segoe UI', 9, 'bold'),
                       bg=color, 
                       fg='white', 
                       border=0, 
                       padx=15, 
                       pady=6, 
                       cursor='hand2',
                       relief='flat',
                       command=command)
        btn.pack(side='left', padx=(0, 5))
    
    # Products display
    products_display_frame = tk.Frame(products_frame, bg=colors['white'])
    products_display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    # Search functionality
    search_frame = tk.Frame(products_display_frame, bg=colors['white'])
    search_frame.pack(fill='x', pady=(0, 10))
    
    tk.Label(search_frame, text="Search:", 
            font=('Segoe UI', 10, 'bold'), bg=colors['white']).pack(side='left')
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                           font=('Segoe UI', 10), width=25)
    search_entry.pack(side='left', padx=(10, 0))
    
    def search_products():
        search_term = search_var.get().lower()
        load_products(search_term)
    
    search_btn = tk.Button(search_frame, text="🔍",
                          font=('Segoe UI', 9),
                          bg=colors['secondary'], fg='white',
                          border=0, padx=10, pady=4,
                          cursor='hand2', relief='flat',
                          command=search_products)
    search_btn.pack(side='left', padx=(5, 0))
    
    search_entry.bind('<KeyRelease>', lambda e: search_products())
    
    # Products listbox
    list_frame = tk.Frame(products_display_frame, bg=colors['white'], relief='solid', bd=1)
    list_frame.pack(fill='both', expand=True)
    
    products_listbox = tk.Listbox(list_frame, 
                                 font=('Segoe UI', 9),
                                 selectbackground=colors['secondary'],
                                 selectforeground='white')
    products_scrollbar = tk.Scrollbar(list_frame, orient='vertical', 
                                     command=products_listbox.yview)
    products_listbox.configure(yscrollcommand=products_scrollbar.set)
    
    products_listbox.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    products_scrollbar.pack(side='right', fill='y')
    
    def load_products(search_term=""):
        try:
            products_listbox.delete(0, tk.END)
            products = read_json(PRODUCT_FILE)
            
            for product in products:
                if (not search_term or 
                    search_term in product.get('name', '').lower() or
                    search_term in product.get('category', '').lower() or
                    search_term in product.get('product_id', '').lower()):
                    
                    stock = product.get('stock', 0)
                    if stock == 0:
                        status = "❌ Out of Stock"
                    elif stock < 5:
                        status = "⚠️ Low Stock"
                    else:
                        status = "✅ In Stock"
                    
                    display_text = (f"[{product['product_id']}] {product['name']} | "
                                  f"${product['price']:.2f} | {product['category']} | "
                                  f"Stock: {stock} ({status})")
                    products_listbox.insert(tk.END, display_text)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products:\n{str(e)}")
    
    # Load initial data
    load_products()

def create_orders_tab(notebook, colors):
    """Create the orders management tab"""
    orders_frame = tk.Frame(notebook, bg=colors['white'])
    notebook.add(orders_frame, text="📋 Orders")
    
    orders_header = tk.Frame(orders_frame, bg=colors['white'])
    orders_header.pack(fill='x', padx=20, pady=15)
    
    orders_title = tk.Label(orders_header,
                           text="Order Management",
                           font=('Segoe UI', 16, 'bold'),
                           bg=colors['white'],
                           fg=colors['primary'])
    orders_title.pack(side='left')
    
    def load_orders():
        try:
            orders_listbox.delete(0, tk.END)
            orders = read_json(ORDER_FILE)
            
            if not orders:
                orders_listbox.insert(tk.END, "No orders found.")
                return
            
            for order_data in orders:
                order = order_data.get('order', {})
                order_id = order.get('order_id', '')[:8] + '...'
                customer = order.get('user_id', 'Unknown')
                items_count = len(order.get('items', []))
                total = f"${order.get('total', 0):.2f}"
                payment = order.get('payment_method', 'Unknown')
                
                display_text = (f"Order {order_id} | Customer: {customer} | "
                              f"{items_count} items | {total} | "
                              f"Payment: {payment} | Status: ✅ Completed")
                orders_listbox.insert(tk.END, display_text)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders:\n{str(e)}")
    
    refresh_btn = tk.Button(orders_header,
                           text="🔄 Refresh",
                           font=('Segoe UI', 10, 'bold'),
                           bg=colors['secondary'],
                           fg='white',
                           border=0,
                           padx=15,
                           pady=8,
                           cursor='hand2',
                           relief='flat',
                           command=load_orders)
    refresh_btn.pack(side='right')
    
    orders_list_frame = tk.Frame(orders_frame, bg=colors['white'], relief='solid', bd=1)
    orders_list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    orders_listbox = tk.Listbox(orders_list_frame, 
                               font=('Segoe UI', 9),
                               selectbackground=colors['secondary'],
                               selectforeground='white')
    orders_scrollbar = tk.Scrollbar(orders_list_frame, orient='vertical', 
                                   command=orders_listbox.yview)
    orders_listbox.configure(yscrollcommand=orders_scrollbar.set)
    
    orders_listbox.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    orders_scrollbar.pack(side='right', fill='y')
    
    # Load initial data
    load_orders()

def create_reports_tab(notebook, colors):
    """Create the reports tab"""
    reports_frame = tk.Frame(notebook, bg=colors['white'])
    notebook.add(reports_frame, text="📊 Reports")
    
    reports_header = tk.Frame(reports_frame, bg=colors['white'])
    reports_header.pack(fill='x', padx=20, pady=15)
    
    reports_title = tk.Label(reports_header,
                            text="Sales Reports & Analytics",
                            font=('Segoe UI', 16, 'bold'),
                            bg=colors['white'],
                            fg=colors['primary'])
    reports_title.pack(side='left')
    
    def generate_sales_report():
        try:
            # Clear previous report
            for widget in reports_display_frame.winfo_children():
                widget.destroy()
                
            orders = read_json(ORDER_FILE)
            
            if not orders:
                no_data_label = tk.Label(reports_display_frame, 
                                       text="📊 No orders found!\n\nStart by processing some orders to see analytics.", 
                                       font=('Segoe UI', 14), 
                                       bg=colors['white'], 
                                       fg=colors['gray'],
                                       justify='center')
                no_data_label.pack(expand=True)
                return
                
            # Calculate statistics
            total_revenue = 0
            product_sales = {}
            
            for order_data in orders:
                order = order_data.get('order', {})
                order_total = order.get('total', 0)
                total_revenue += order_total
                
                # Product analysis
                for item in order.get('items', []):
                    pid = item.get('product_id', 'Unknown')
                    name = item.get('name', 'Unknown')
                    qty = item.get('quantity', 0)
                    price = item.get('price', 0)
                    
                    if pid in product_sales:
                        product_sales[pid]['qty'] += qty
                        product_sales[pid]['revenue'] += price * qty
                    else:
                        product_sales[pid] = {
                            'name': name,
                            'qty': qty,
                            'revenue': price * qty
                        }
            
            # Create report display
            report_content = tk.Frame(reports_display_frame, bg=colors['white'])
            report_content.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Report title
            report_title = tk.Label(report_content, 
                                   text="📊 Sales Analytics Report", 
                                   font=('Segoe UI', 16, 'bold'), 
                                   bg=colors['white'], 
                                   fg=colors['primary'])
            report_title.pack(pady=(0, 15))
            
            # Summary
            summary_frame = tk.Frame(report_content, bg=colors['light'])
            summary_frame.pack(fill='x', pady=(0, 15))
            
            avg_order_value = total_revenue / len(orders) if orders else 0
            total_items_sold = sum(data['qty'] for data in product_sales.values())
            
            summary_text = (f"Total Orders: {len(orders)} | "
                           f"Total Revenue: ${total_revenue:.2f} | "
                           f"Average Order: ${avg_order_value:.2f} | "
                           f"Items Sold: {total_items_sold}")
            
            tk.Label(summary_frame, text=summary_text, 
                    font=('Segoe UI', 11, 'bold'), 
                    bg=colors['light'], fg=colors['primary'],
                    padx=15, pady=10).pack()
            
            # Top products
            if product_sales:
                products_section = tk.LabelFrame(report_content, 
                                               text="Top Selling Products", 
                                               font=('Segoe UI', 12, 'bold'), 
                                               bg=colors['white'],
                                               fg=colors['primary'])
                products_section.pack(fill='both', expand=True, pady=(10, 0))
                
                # Sort products by revenue
                sorted_products = sorted(product_sales.items(), 
                                       key=lambda x: x[1]['revenue'], reverse=True)
                
                sales_listbox = tk.Listbox(products_section, 
                                         font=('Segoe UI', 10), 
                                         height=8,
                                         selectbackground=colors['secondary'],
                                         selectforeground='white')
                
                sales_listbox.pack(fill='both', expand=True, padx=10, pady=10)
                
                for i, (pid, data) in enumerate(sorted_products[:10], 1):
                    display_text = (f"{i}. {data['name']} | "
                                  f"{data['qty']} units sold | "
                                  f"${data['revenue']:.2f} revenue")
                    sales_listbox.insert(tk.END, display_text)
                    
        except Exception as e:
            error_label = tk.Label(reports_display_frame, 
                                 text=f"⚠️ Error generating report:\n{str(e)}", 
                                 font=('Segoe UI', 12), 
                                 bg=colors['white'], 
                                 fg=colors['danger'],
                                 justify='center')
            error_label.pack(expand=True)
    
    generate_btn = tk.Button(reports_header,
                            text="📊 Generate Report",
                            font=('Segoe UI', 10, 'bold'),
                            bg=colors['success'],
                            fg='white',
                            border=0,
                            padx=15,
                            pady=8,
                            cursor='hand2',
                            relief='flat',
                            command=generate_sales_report)
    generate_btn.pack(side='right')
    
    # Reports display area
    reports_display_frame = tk.Frame(reports_frame, bg=colors['white'], relief='solid', bd=1)
    reports_display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
    
    # Initial message
    initial_label = tk.Label(reports_display_frame, 
                            text="📊 Click 'Generate Report' to view comprehensive sales analytics", 
                            font=('Segoe UI', 12), 
                            bg=colors['white'], 
                            fg=colors['gray'],
                            justify='center')
    initial_label.pack(expand=True)

class ProductDialog(tk.Toplevel):
    """Enhanced Product Dialog with Proper Sizing and Scrolling"""
    def __init__(self, parent, title, product_data=None):
        super().__init__(parent)
        self.result = None
        self.product_data = product_data or {}
        
        self.title(title)
        
        # Start with a reasonable size but allow dynamic sizing
        self.geometry("550x750")
        self.resizable(True, True)
        
        # Modern colors
        colors = {
            'primary': '#2c3e50',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'white': '#ffffff',
            'light': '#ecf0f1'
        }
        
        self.configure(bg=colors['white'])
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets(colors)
        
        # Center and auto-resize after creation
        self.after(100, self.center_and_resize)
        
        # Wait for dialog to close
        parent.wait_window(self)
        
    def center_and_resize(self):
        """Center dialog and auto-resize to fit content"""
        try:
            self.update_idletasks()
            
            # Get the required size
            req_width = self.winfo_reqwidth()
            req_height = self.winfo_reqheight()
            
            # Set minimum sizes and add padding
            width = max(550, req_width + 50)
            height = max(650, min(800, req_height + 100))  # Cap at 800px
            
            # Center on screen
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            
            self.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            print(f"DEBUG: Dialog resize error: {e}")
        
    def create_widgets(self, colors):
        # Header
        header_frame = tk.Frame(self, bg=colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_text = "Edit Product" if self.product_data else "Add New Product"
        title_label = tk.Label(header_frame, 
                              text=title_text, 
                              font=('Segoe UI', 14, 'bold'), 
                              bg=colors['primary'], 
                              fg='white')
        title_label.pack(expand=True)
        
        # Create main frame with scrolling capability
        main_frame = tk.Frame(self, bg=colors['white'])
        main_frame.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg=colors['white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form content inside scrollable frame
        form_frame = tk.Frame(scrollable_frame, bg=colors['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        self.entries = {}
        fields = [
            ("Product ID:", "product_id", "e.g., P001"),
            ("Product Name:", "name", "e.g., Gaming Laptop"),
            ("Price ($):", "price", "e.g., 999.99"),
            ("Category:", "category", "e.g., Computers"),
            ("Stock Quantity:", "stock", "e.g., 50"),
            ("Description:", "description", "Product description (optional)")
        ]
        
        for label_text, field_name, placeholder in fields:
            # Label
            label = tk.Label(form_frame, 
                           text=label_text, 
                           font=('Segoe UI', 10, 'bold'), 
                           bg=colors['white'])
            label.pack(anchor='w', pady=(10, 2))
            
            # Entry or Text widget for description
            if field_name == "description":
                entry = tk.Text(form_frame, 
                              font=('Segoe UI', 10), 
                              relief='solid', 
                              bd=1,
                              height=4,
                              wrap='word')
            else:
                entry = tk.Entry(form_frame, 
                               font=('Segoe UI', 10), 
                               relief='solid', 
                               bd=1)
            
            entry.pack(fill='x', pady=(0, 2), ipady=6)
            
            # Placeholder
            placeholder_label = tk.Label(form_frame,
                                       text=placeholder,
                                       font=('Segoe UI', 8),
                                       bg=colors['white'],
                                       fg='#95a5a6')
            placeholder_label.pack(anchor='w', pady=(0, 5))
            
            self.entries[field_name] = entry
            
            # Pre-fill if editing
            if self.product_data and field_name in self.product_data:
                if field_name == "description":
                    entry.insert('1.0', str(self.product_data[field_name]))
                else:
                    entry.insert(0, str(self.product_data[field_name]))
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg=colors['white'])
        button_frame.pack(fill='x', pady=30)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, 
                              text="❌ Cancel", 
                              font=('Segoe UI', 11, 'bold'),
                              bg=colors['danger'], 
                              fg='white', 
                              border=0, 
                              padx=25, 
                              pady=10,
                              cursor='hand2',
                              relief='flat',
                              command=self.cancel)
        cancel_btn.pack(side='right', padx=(15, 0))
        
        # Save button
        save_text = "✅ Update" if self.product_data else "✅ Save"
        save_btn = tk.Button(button_frame, 
                            text=save_text, 
                            font=('Segoe UI', 11, 'bold'),
                            bg=colors['success'], 
                            fg='white', 
                            border=0, 
                            padx=30, 
                            pady=10,
                            cursor='hand2',
                            relief='flat',
                            command=self.save)
        save_btn.pack(side='right')
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
        # Focus on first field
        self.entries['product_id'].focus()
        
    def save(self):
        try:
            # Validate inputs
            product_id = self.entries['product_id'].get().strip()
            name = self.entries['name'].get().strip()
            price_str = self.entries['price'].get().strip()
            category = self.entries['category'].get().strip()
            stock_str = self.entries['stock'].get().strip()
            
            # Get description (from Text widget)
            if isinstance(self.entries['description'], tk.Text):
                description = self.entries['description'].get('1.0', tk.END).strip()
            else:
                description = self.entries['description'].get().strip()
            
            # Check required fields
            if not all([product_id, name, price_str, category, stock_str]):
                messagebox.showerror("Missing Information", "Please fill in all required fields!")
                return
            
            # Validate price
            try:
                price = float(price_str)
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except ValueError:
                messagebox.showerror("Invalid Price", "Please enter a valid price!")
                return
            
            # Validate stock
            try:
                stock = int(stock_str)
                if stock < 0:
                    raise ValueError("Stock cannot be negative")
            except ValueError:
                messagebox.showerror("Invalid Stock", "Please enter a valid stock quantity!")
                return
                
            self.result = {
                'product_id': product_id,
                'name': name,
                'price': price,
                'category': category,
                'stock': stock,
                'description': description
            }
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product:\n{str(e)}")
            
    def cancel(self):
        self.destroy()

if __name__ == "__main__":
    admin_gui()