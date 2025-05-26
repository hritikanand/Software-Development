import uuid
from datetime import datetime

class Invoice:
    """Invoice model for order billing"""
    
    def __init__(self, order):
        self.invoice_id = str(uuid.uuid4())
        self.order_id = order.order_id
        self.user_id = order.user_id
        self.amount = order.calculate_total()
        self.subtotal = order.calculate_subtotal()
        self.tax_amount = 0.0  # Can be calculated later if needed
        self.total_amount = self.amount + self.tax_amount
        self.invoice_date = datetime.now().isoformat()
        self.due_date = datetime.now().isoformat()  # Immediate payment
        self.status = "Generated"
        self.items = order.items.copy()
        self.shipping_info = order.shipping.copy()
    
    def calculate_tax(self, tax_rate=0.10):
        """Calculate tax amount based on rate"""
        self.tax_amount = self.subtotal * tax_rate
        self.total_amount = self.subtotal + self.tax_amount
        return self.tax_amount
    
    def mark_as_paid(self):
        """Mark invoice as paid"""
        self.status = "Paid"
        return True
    
    def mark_as_overdue(self):
        """Mark invoice as overdue"""
        self.status = "Overdue"
        return True
    
    def is_paid(self):
        """Check if invoice is paid"""
        return self.status == "Paid"
    
    def get_invoice_summary(self):
        """Get invoice summary"""
        return {
            "invoice_id": self.invoice_id[:8] + "...",
            "order_id": self.order_id[:8] + "...",
            "amount": self.amount,
            "tax": self.tax_amount,
            "total": self.total_amount,
            "status": self.status,
            "date": self.invoice_date
        }
    
    def get_line_items(self):
        """Get detailed line items"""
        line_items = []
        for item in self.items:
            line_total = item["price"] * item["quantity"]
            line_items.append({
                "product_id": item["product_id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "total": line_total
            })
        return line_items
    
    def add_discount(self, discount_amount, description="Discount"):
        """Add discount to invoice"""
        self.discount_amount = discount_amount
        self.discount_description = description
        self.total_amount = self.subtotal + self.tax_amount - discount_amount
        return True
    
    def generate_invoice_number(self, prefix="INV"):
        """Generate human-readable invoice number"""
        date_str = datetime.now().strftime("%Y%m%d")
        short_id = self.invoice_id[:8].upper()
        return f"{prefix}-{date_str}-{short_id}"

    def to_dict(self):
        """Convert invoice to dictionary for JSON storage"""
        return {
            "invoice_id": self.invoice_id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "status": self.status,
            "items": self.items,
            "shipping_info": self.shipping_info
        }
    
    @classmethod
    def from_dict(cls, data, order=None):
        """Create Invoice instance from dictionary"""
        # Create a minimal order object if not provided
        if order is None:
            class MinimalOrder:
                def __init__(self, data):
                    self.order_id = data["order_id"]
                    self.user_id = data["user_id"]
                    self.items = data.get("items", [])
                    self.shipping = data.get("shipping_info", {})
                
                def calculate_total(self):
                    return data["amount"]
                
                def calculate_subtotal(self):
                    return data.get("subtotal", data["amount"])
            
            order = MinimalOrder(data)
        
        invoice = cls(order)
        invoice.invoice_id = data["invoice_id"]
        invoice.subtotal = data.get("subtotal", data["amount"])
        invoice.tax_amount = data.get("tax_amount", 0.0)
        invoice.total_amount = data.get("total_amount", data["amount"])
        invoice.invoice_date = data.get("invoice_date", datetime.now().isoformat())
        invoice.due_date = data.get("due_date", datetime.now().isoformat())
        invoice.status = data.get("status", "Generated")
        return invoice

    def __str__(self):
        return f"Invoice {self.invoice_id[:8]}... - ${self.total_amount:.2f} - {self.status}"
    
    def __repr__(self):
        return f"Invoice(id={self.invoice_id[:8]}..., amount={self.total_amount:.2f}, status='{self.status}')"