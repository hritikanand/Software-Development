# models/receipt.py
import uuid

class Receipt:
    def __init__(self, invoice, payment_method):
        self.receipt_id = str(uuid.uuid4())
        self.invoice_id = invoice.invoice_id
        self.payment_method = payment_method
        self.status = "Paid"

    def to_dict(self):
        return {
            "receipt_id": self.receipt_id,
            "invoice_id": self.invoice_id,
            "payment_method": self.payment_method,
            "status": self.status
        }
