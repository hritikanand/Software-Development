import uuid
from datetime import datetime

class Order:
    """Order model for managing customer orders"""
    
    def __init__(self, user_id, items, shipping, payment_method):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = items  # List of dicts with product_id, name, price, quantity
        self.shipping = shipping  # Dict with name, address, phone
        self.payment_method = payment_method
        self.order_date = datetime.now().isoformat()
        self.status = "Confirmed"

    def calculate_total(self):
        """Calculate total order amount"""
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def calculate_subtotal(self):
        """Calculate subtotal (same as total for now, but could include taxes later)"""
        return self.calculate_total()
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item["quantity"] for item in self.items)
    
    def get_order_summary(self):
        """Get a summary of the order"""
        return {
            "order_id": self.order_id[:8] + "...",
            "customer": self.user_id,
            "items_count": self.get_total_items(),
            "total": self.calculate_total(),
            "status": self.status,
            "date": self.order_date
        }
    
    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = ["Pending", "Confirmed", "Processing", "Shipped", "Delivered", "Cancelled"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False
    
    def add_item(self, product_id, name, price, quantity):
        """Add item to order"""
        self.items.append({
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity
        })
    
    def remove_item(self, product_id):
        """Remove item from order"""
        self.items = [item for item in self.items if item["product_id"] != product_id]
    
    def get_shipping_info(self):
        """Get shipping information"""
        return self.shipping.copy()
    
    def update_shipping(self, shipping_info):
        """Update shipping information"""
        self.shipping.update(shipping_info)

    def to_dict(self):
        """Convert order to dictionary for JSON storage"""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": self.items,
            "shipping": self.shipping,
            "payment_method": self.payment_method,
            "total": self.calculate_total(),
            "order_date": self.order_date,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Order instance from dictionary"""
        order = cls(
            user_id=data["user_id"],
            items=data["items"],
            shipping=data["shipping"],
            payment_method=data["payment_method"]
        )
        order.order_id = data["order_id"]
        order.order_date = data.get("order_date", datetime.now().isoformat())
        order.status = data.get("status", "Confirmed")
        return order

    def __str__(self):
        return f"Order {self.order_id[:8]}... - {self.user_id} - ${self.calculate_total():.2f}"
    
    def __repr__(self):
        return f"Order(id={self.order_id[:8]}..., user={self.user_id}, total={self.calculate_total():.2f})"