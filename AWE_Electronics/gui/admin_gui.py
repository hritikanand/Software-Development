import tkinter as tk
from tkinter import messagebox, simpledialog
from utils.file_handler import read_json, write_json

PRODUCT_FILE = "data/products.json"
ORDER_FILE = "data/orders.json"

def admin_gui():
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("400x400")

    # ===== Admin Feature Functions =====

    def view_products():
        products = read_json(PRODUCT_FILE)
        view_win = tk.Toplevel()
        view_win.title("All Products")
        view_win.geometry("400x300")
        for p in products:
            text = f"[{p['product_id']}] {p['name']} - ${p['price']} ({p['stock']} in stock)"
            tk.Label(view_win, text=text).pack(anchor="w")

    def add_product():
        products = read_json(PRODUCT_FILE)

        pid = simpledialog.askstring("Add Product", "Enter Product ID:")
        if any(p['product_id'] == pid for p in products):
            messagebox.showerror("Error", "Product ID already exists.")
            return

        name = simpledialog.askstring("Add Product", "Product Name:")
        price = simpledialog.askfloat("Add Product", "Price:")
        category = simpledialog.askstring("Add Product", "Category:")
        stock = simpledialog.askinteger("Add Product", "Stock Quantity:")

        new_product = {
            "product_id": pid,
            "name": name,
            "price": price,
            "category": category,
            "stock": stock
        }

        products.append(new_product)
        write_json(PRODUCT_FILE, products)
        messagebox.showinfo("Success", "Product added successfully.")

    def update_stock():
        products = read_json(PRODUCT_FILE)
        pid = simpledialog.askstring("Update Stock", "Enter Product ID:")

        for p in products:
            if p["product_id"] == pid:
                new_stock = simpledialog.askinteger("Update Stock", f"Enter new stock for {p['name']}:")
                p["stock"] = new_stock
                write_json(PRODUCT_FILE, products)
                messagebox.showinfo("Success", "Stock updated.")
                return

        messagebox.showerror("Error", "Product not found.")

    def delete_product():
        products = read_json(PRODUCT_FILE)
        pid = simpledialog.askstring("Delete Product", "Enter Product ID to delete:")

        new_list = [p for p in products if p["product_id"] != pid]
        if len(new_list) != len(products):
            write_json(PRODUCT_FILE, new_list)
            messagebox.showinfo("Success", "Product deleted.")
        else:
            messagebox.showerror("Error", "Product not found.")

    def sales_report():
        orders = read_json(ORDER_FILE)
        total_sales = 0
        product_sales = {}

        for entry in orders:
            for item in entry["order"]["items"]:
                pid = item["product_id"]
                qty = item["quantity"]
                total_sales += item["price"] * qty
                if pid in product_sales:
                    product_sales[pid]["qty"] += qty
                else:
                    product_sales[pid] = {"name": item["name"], "qty": qty}

        report_win = tk.Toplevel()
        report_win.title("Sales Report")
        report_win.geometry("400x300")

        for pid, data in product_sales.items():
            text = f"{data['name']} - {data['qty']} units sold"
            tk.Label(report_win, text=text).pack(anchor="w")

        tk.Label(report_win, text=f"\nTotal Revenue: ${total_sales:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    # ===== Admin Menu Layout =====

    tk.Label(root, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="View Products", width=25, command=view_products).pack(pady=5)
    tk.Button(root, text="Add New Product", width=25, command=add_product).pack(pady=5)
    tk.Button(root, text="Update Product Stock", width=25, command=update_stock).pack(pady=5)
    tk.Button(root, text="Delete Product", width=25, command=delete_product).pack(pady=5)
    tk.Button(root, text="Generate Sales Report", width=25, command=sales_report).pack(pady=10)

    # ✅ Logout Button
    tk.Button(root, text="Logout", width=25, fg="red", command=root.destroy).pack(pady=10)

    root.mainloop()
