# models/order.py
import uuid

class Order:
    def __init__(self, user_id, items, shipping, payment_method):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = items
        self.shipping = shipping
        self.payment_method = payment_method

    def calculate_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": self.items,
            "shipping": self.shipping,
            "payment_method": self.payment_method,
            "total": self.calculate_total()
        }
