from models.order import Order
from models.invoice import Invoice
from models.receipt import Receipt
from models.shipping import collect_shipping_details
from models.payment import choose_payment_method
from utils.file_handler import write_json, read_json
from models.catalogue import Catalogue

ORDER_FILE = "data/orders.json"

def checkout(user):
    if not user["cart"]:
        print(" Your cart is empty.")
        return

    # Load all products
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

    # Get shipping and payment info
    shipping = collect_shipping_details()
    payment_method = choose_payment_method()

    # Create order, invoice, and receipt
    order = Order(user["username"], items, shipping, payment_method)
    invoice = Invoice(order)
    receipt = Receipt(invoice, payment_method)

    # Save to orders.json
    orders = read_json(ORDER_FILE)
    orders.append({
        "order": order.to_dict(),
        "invoice": invoice.to_dict(),
        "receipt": receipt.to_dict()
    })
    write_json(ORDER_FILE, orders)

    # Clear cart after successful order
    user["cart"] = []

    print("\n Order Placed Successfully!")
    print(f" Invoice Total: ${invoice.amount}")
    print(f" Receipt ID: {receipt.receipt_id}")
