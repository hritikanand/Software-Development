# controllers/cart_controller.py
from utils.file_handler import read_json
from models.catalogue import Catalogue

PRODUCT_FILE = "data/products.json"

def add_to_cart(user):
    cat = Catalogue()
    pid = input("Enter product ID to add: ")
    quantity = int(input("Enter quantity: "))

    product = next((p for p in cat.products if p.product_id == pid), None)
    if product and product.stock >= quantity:
        user["cart"].append({"product_id": pid, "quantity": quantity})
        print(f"✅ Added {quantity} of '{product.name}' to cart.")
    else:
        print("❌ Product not found or insufficient stock.")

def view_cart(user):
    if not user["cart"]:
        print("🛒 Your cart is empty.")
        return

    print("\n🧺 Current Cart:")
    cat = Catalogue()
    total = 0
    for item in user["cart"]:
        prod = next((p for p in cat.products if p.product_id == item["product_id"]), None)
        if prod:
            subtotal = prod.price * item["quantity"]
            print(f"{prod.name} x {item['quantity']} = ${subtotal}")
            total += subtotal
    print(f"💰 Total: ${total}")
