from utils.file_handler import read_json, write_json

PRODUCT_FILE = "data/products.json"
ORDER_FILE = "data/orders.json"

def view_products():
    print("\n Current Product List:")
    products = read_json(PRODUCT_FILE)
    for p in products:
        print(f"[{p['product_id']}] {p['name']} - ${p['price']} ({p['stock']} in stock)")

def add_product():
    products = read_json(PRODUCT_FILE)
    product_id = input("Enter new product ID: ")
    if any(p['product_id'] == product_id for p in products):
        print(" Product ID already exists.")
        return
    name = input("Product name: ")
    price = float(input("Price: "))
    category = input("Category: ")
    stock = int(input("Stock quantity: "))

    new_product = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "category": category,
        "stock": stock
    }
    products.append(new_product)
    write_json(PRODUCT_FILE, products)
    print(" Product added successfully.")

def update_stock():
    products = read_json(PRODUCT_FILE)
    product_id = input("Enter product ID to update: ")
    for p in products:
        if p['product_id'] == product_id:
            new_stock = int(input(f"Enter new stock for '{p['name']}': "))
            p['stock'] = new_stock
            write_json(PRODUCT_FILE, products)
            print(" Stock updated.")
            return
    print(" Product not found.")

def delete_product():
    products = read_json(PRODUCT_FILE)
    product_id = input("Enter product ID to delete: ")
    new_list = [p for p in products if p['product_id'] != product_id]
    if len(new_list) != len(products):
        write_json(PRODUCT_FILE, new_list)
        print(" Product deleted.")
    else:
        print(" Product not found.")

def generate_sales_report():
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

    print("\n Sales Report")
    for pid, data in product_sales.items():
        print(f"{data['name']} - {data['qty']} units sold")
    print(f"\n💰 Total Revenue: ${total_sales:.2f}")
