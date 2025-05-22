# models/product.py
class Product:
    def __init__(self, product_id, name, price, category, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock": self.stock
        }

    def __str__(self):
        return f"[{self.product_id}] {self.name} - ${self.price} ({self.stock} left)"
