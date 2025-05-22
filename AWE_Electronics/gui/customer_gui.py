import tkinter as tk
from tkinter import messagebox
from models.catalogue import Catalogue
from controllers.product_controller import browse_products
from controllers.cart_controller import view_cart
from models.order import Order
from models.invoice import Invoice
from models.receipt import Receipt
from utils.file_handler import read_json, write_json

ORDER_FILE = "data/orders.json"

def customer_gui(user):
    window = tk.Tk()
    window.title(f"Customer Dashboard - {user['username']}")
    window.geometry("450x450")

    def browse():
        cat = Catalogue()
        product_window = tk.Toplevel()
        product_window.title("Available Products")
        product_window.geometry("400x300")

        for product in cat.list_all_products():
            product_str = f"[{product.product_id}] {product.name} - ${product.price} ({product.stock} in stock)"
            tk.Label(product_window, text=product_str).pack(anchor="w")

    def add_to_cart_gui():
        pid = pid_entry.get()
        try:
            qty = int(qty_entry.get())
            user["cart"].append({"product_id": pid, "quantity": qty})
            messagebox.showinfo("Success", f"Added {qty} of {pid} to cart.")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")

    def view_cart_gui():
        cart_window = tk.Toplevel()
        cart_window.title("Your Cart")
        cart_window.geometry("400x300")

        cat = Catalogue()
        total = 0

        for item in user["cart"]:
            prod = next((p for p in cat.products if p.product_id == item["product_id"]), None)
            if prod:
                subtotal = prod.price * item["quantity"]
                total += subtotal
                item_str = f"{prod.name} x {item['quantity']} = ${subtotal}"
                tk.Label(cart_window, text=item_str).pack(anchor="w")

        tk.Label(cart_window, text=f"\nTotal: ${total:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    def checkout_gui():
        shipping_win = tk.Toplevel()
        shipping_win.title("Shipping Info")
        shipping_win.geometry("350x300")

        tk.Label(shipping_win, text="Enter Shipping Details", font=("Arial", 12)).pack(pady=5)

        labels = ["Full Name", "Address", "Phone Number"]
        entries = {}

        for label in labels:
            tk.Label(shipping_win, text=label).pack()
            entry = tk.Entry(shipping_win)
            entry.pack()
            entries[label] = entry

        def go_to_payment():
            shipping = {
                "name": entries["Full Name"].get(),
                "address": entries["Address"].get(),
                "phone": entries["Phone Number"].get()
            }
            shipping_win.destroy()
            payment_gui(shipping)

        tk.Button(shipping_win, text="Continue to Payment", command=go_to_payment).pack(pady=10)

    def payment_gui(shipping):
        pay_win = tk.Toplevel()
        pay_win.title("Payment Method")
        pay_win.geometry("350x250")

        tk.Label(pay_win, text="Choose Payment Method", font=("Arial", 12)).pack(pady=5)

        method_var = tk.StringVar()
        method_var.set("PayPal")

        tk.Radiobutton(pay_win, text="PayPal", variable=method_var, value="PayPal").pack()
        tk.Radiobutton(pay_win, text="Credit Card", variable=method_var, value="Credit Card").pack()

        tk.Label(pay_win, text="Account/Cardholder Name:").pack()
        name_entry = tk.Entry(pay_win)
        name_entry.pack()

        def confirm_order():
            payment_method = f"{method_var.get()} - {name_entry.get()}"
            cat = Catalogue()
            items = []

            for entry in user["cart"]:
                prod = next((p for p in cat.products if p.product_id == entry["product_id"]), None)
                if prod:
                    items.append({
                        "product_id": prod.product_id,
                        "name": prod.name,
                        "price": prod.price,
                        "quantity": entry["quantity"]
                    })

            order = Order(user["username"], items, shipping, payment_method)
            invoice = Invoice(order)
            receipt = Receipt(invoice, payment_method)

            orders = read_json(ORDER_FILE)
            orders.append({
                "order": order.to_dict(),
                "invoice": invoice.to_dict(),
                "receipt": receipt.to_dict()
            })
            write_json(ORDER_FILE, orders)

            user["cart"] = []

            messagebox.showinfo(
                "Order Placed",
                f"✅ Order Placed Successfully!\n\n🧾 Invoice Total: ${invoice.amount}\n📄 Receipt ID: {receipt.receipt_id}"
            )
            pay_win.destroy()

        tk.Button(pay_win, text="Place Order", command=confirm_order).pack(pady=15)

    # GUI Layout
    tk.Label(window, text="Customer Dashboard", font=("Arial", 16)).pack(pady=10)

    tk.Button(window, text="Browse Products", width=25, command=browse).pack(pady=5)

    tk.Label(window, text="Product ID:").pack()
    pid_entry = tk.Entry(window)
    pid_entry.pack()

    tk.Label(window, text="Quantity:").pack()
    qty_entry = tk.Entry(window)
    qty_entry.pack()

    tk.Button(window, text="Add to Cart", width=25, command=add_to_cart_gui).pack(pady=5)
    tk.Button(window, text="View Cart", width=25, command=view_cart_gui).pack(pady=5)
    tk.Button(window, text="Checkout", width=25, command=checkout_gui).pack(pady=10)
    tk.Button(window, text="Logout", width=25, command=window.destroy, fg="red").pack(pady=5)

    window.mainloop()
