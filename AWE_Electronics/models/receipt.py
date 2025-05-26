import uuid
from datetime import datetime

class Receipt:
    """Receipt model for payment confirmation"""
    
    def __init__(self, invoice, payment_method):
        self.receipt_id = str(uuid.uuid4())
        self.invoice_id = invoice.invoice_id
        self.order_id = invoice.order_id
        self.user_id = invoice.user_id
        self.payment_method = payment_method
        self.amount_paid = invoice.total_amount
        self.payment_date = datetime.now().isoformat()
        self.status = "Paid"
        self.transaction_reference = self.generate_transaction_reference()
        
        # Copy invoice details for receipt
        self.items = invoice.items.copy()
        self.subtotal = invoice.subtotal
        self.tax_amount = invoice.tax_amount
        self.total_amount = invoice.total_amount
        self.shipping_info = invoice.shipping_info.copy()
    
    def generate_transaction_reference(self):
        """Generate transaction reference number"""
        date_str = datetime.now().strftime("%Y%m%d%H%M")
        short_id = self.receipt_id[:6].upper()
        return f"TXN-{date_str}-{short_id}"
    
    def generate_receipt_number(self, prefix="RCP"):
        """Generate human-readable receipt number"""
        date_str = datetime.now().strftime("%Y%m%d")
        short_id = self.receipt_id[:8].upper()
        return f"{prefix}-{date_str}-{short_id}"
    
    def get_payment_summary(self):
        """Get payment summary"""
        return {
            "receipt_id": self.receipt_id[:8] + "...",
            "transaction_ref": self.transaction_reference,
            "payment_method": self.payment_method,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date,
            "status": self.status
        }
    
    def get_receipt_details(self):
        """Get complete receipt details"""
        return {
            "receipt_number": self.generate_receipt_number(),
            "receipt_id": self.receipt_id,
            "order_id": self.order_id,
            "invoice_id": self.invoice_id,
            "customer": self.user_id,
            "payment_method": self.payment_method,
            "transaction_reference": self.transaction_reference,
            "items": self.get_itemized_list(),
            "subtotal": self.subtotal,
            "tax": self.tax_amount,
            "total": self.total_amount,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date,
            "status": self.status,
            "shipping": self.shipping_info
        }
    
    def get_itemized_list(self):
        """Get itemized list with calculations"""
        itemized = []
        for item in self.items:
            line_total = item["price"] * item["quantity"]
            itemized.append({
                "product_id": item["product_id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "line_total": line_total
            })
        return itemized
    
    def mark_as_refunded(self, refund_amount=None):
        """Mark receipt as refunded"""
        self.status = "Refunded"
        if refund_amount:
            self.refund_amount = refund_amount
        else:
            self.refund_amount = self.amount_paid
        self.refund_date = datetime.now().isoformat()
        return True
    
    def is_paid(self):
        """Check if payment is completed"""
        return self.status == "Paid"
    
    def is_refunded(self):
        """Check if payment is refunded"""
        return self.status == "Refunded"
    
    def validate_payment(self):
        """Validate payment amount matches invoice"""
        return abs(self.amount_paid - self.total_amount) < 0.01  # Allow for small rounding differences
    
    def get_change_amount(self):
        """Calculate change if overpaid"""
        return max(0, self.amount_paid - self.total_amount)

    def to_dict(self):
        """Convert receipt to dictionary for JSON storage"""
        return {
            "receipt_id": self.receipt_id,
            "invoice_id": self.invoice_id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "payment_method": self.payment_method,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date,
            "status": self.status,
            "transaction_reference": self.transaction_reference,
            "items": self.items,
            "subtotal": self.subtotal,    
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount,
            "shipping_info": self.shipping_info
        }
    
    @classmethod
    def from_dict(cls, data, invoice=None):
        """Create Receipt instance from dictionary"""
        # Create a minimal invoice object if not provided
        if invoice is None:
            class MinimalInvoice:
                def __init__(self, data):
                    self.invoice_id = data["invoice_id"]
                    self.order_id = data["order_id"]
                    self.user_id = data["user_id"]
                    self.items = data.get("items", [])
                    self.subtotal = data.get("subtotal", 0)
                    self.tax_amount = data.get("tax_amount", 0)
                    self.total_amount = data.get("total_amount", data.get("amount_paid", 0))
                    self.shipping_info = data.get("shipping_info", {})
            
            invoice = MinimalInvoice(data)
        
        receipt = cls(invoice, data["payment_method"])
        receipt.receipt_id = data["receipt_id"]
        receipt.amount_paid = data["amount_paid"]
        receipt.payment_date = data.get("payment_date", datetime.now().isoformat())
        receipt.status = data.get("status", "Paid")
        receipt.transaction_reference = data.get("transaction_reference", receipt.generate_transaction_reference())
        return receipt

    def __str__(self):
        return f"Receipt {self.receipt_id[:8]}... - ${self.amount_paid:.2f} - {self.payment_method} - {self.status}"
    
    def __repr__(self):
        return f"Receipt(id={self.receipt_id[:8]}..., amount={self.amount_paid:.2f}, method='{self.payment_method}', status='{self.status}')"