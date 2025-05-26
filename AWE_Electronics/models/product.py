class Product:
    """Product model for inventory management"""
    
    def __init__(self, product_id, name, price, category, stock, description=""):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.category = category
        self.stock = int(stock)
        self.description = description

    def to_dict(self):
        """Convert product to dictionary for JSON storage"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock": self.stock,
            "description": self.description
        }
    
    def is_available(self, quantity=1):
        """Check if product is available in requested quantity"""
        return self.stock >= quantity
    
    def is_low_stock(self, threshold=5):
        """Check if product is low in stock"""
        return self.stock <= threshold
    
    def update_stock(self, new_stock):
        """Update product stock"""
        self.stock = max(0, int(new_stock))
    
    def reduce_stock(self, quantity):
        """Reduce stock by specified quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def get_stock_status(self):
        """Get stock status as a readable string"""
        if self.stock == 0:
            return "Out of Stock"
        elif self.stock <= 5:
            return "Low Stock"
        else:
            return "In Stock"

    def __str__(self):
        return f"[{self.product_id}] {self.name} - ${self.price} ({self.stock} left)"
    
    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.name}', price={self.price}, stock={self.stock})"