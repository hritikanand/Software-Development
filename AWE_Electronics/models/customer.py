from models.account import Account

class Customer(Account):
    """Customer account class extending base Account"""
    
    def __init__(self, username, password, email, address, phone_number, full_name=""):
        super().__init__(username, password, email, "customer")
        self.address = address
        self.phone_number = phone_number
        self.full_name = full_name
        self.cart = []

    def to_dict(self):
        """Convert customer to dictionary for JSON storage"""
        data = super().to_dict()
        data.update({
            "address": self.address,
            "phone_number": self.phone_number,
            "full_name": self.full_name,
            "cart": self.cart
        })
        return data
    
    def add_to_cart(self, product_id, quantity=1):
        """Add item to shopping cart"""
        # Check if item already exists in cart
        for item in self.cart:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return
        
        # Add new item to cart
        self.cart.append({
            "product_id": product_id,
            "quantity": quantity
        })
    
    def remove_from_cart(self, product_id):
        """Remove item from shopping cart"""
        self.cart = [item for item in self.cart if item["product_id"] != product_id]
    
    def update_cart_quantity(self, product_id, quantity):
        """Update quantity of item in cart"""
        for item in self.cart:
            if item["product_id"] == product_id:
                if quantity <= 0:
                    self.remove_from_cart(product_id)
                else:
                    item["quantity"] = quantity
                return True
        return False
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart = []
    
    def get_cart_total_items(self):
        """Get total number of items in cart"""
        return sum(item["quantity"] for item in self.cart)
    
    def get_cart_items(self):
        """Get list of cart items"""
        return self.cart.copy()
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return len(self.cart) == 0
    
    def update_profile(self, **kwargs):
        """Update customer profile information"""
        if "address" in kwargs:
            self.address = kwargs["address"]
        if "phone_number" in kwargs:
            self.phone_number = kwargs["phone_number"]
        if "full_name" in kwargs:
            self.full_name = kwargs["full_name"]
        if "email" in kwargs:
            self.email = kwargs["email"]

    def __str__(self):
        return f"Customer(username={self.username}, email={self.email}, cart_items={self.get_cart_total_items()})"
    
    def __repr__(self):
        return self.__str__()