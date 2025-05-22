import uuid

class Invoice:
    def __init__(self, order):
        self.invoice_id = str(uuid.uuid4())
        self.order_id = order.order_id
        self.amount = order.calculate_total()

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "order_id": self.order_id,
            "amount": self.amount
        }
