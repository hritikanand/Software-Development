from utils.file_handler import read_json
from models.product import Product

PRODUCT_FILE = "data/products.json"

class Catalogue:
    """Product catalogue management class"""
    
    def __init__(self):
        self.products = []
        self.load_products()

    def load_products(self):
        """Load products from JSON file"""
        try:
            product_data = read_json(PRODUCT_FILE)
            self.products = []
            
            for prod_dict in product_data:
                # Handle both old and new data formats
                description = prod_dict.get('description', '')
                product = Product(
                    product_id=prod_dict['product_id'],
                    name=prod_dict['name'],
                    price=prod_dict['price'],
                    category=prod_dict['category'],
                    stock=prod_dict['stock'],
                    description=description
                )
                self.products.append(product)
                
        except Exception as e:
            print(f"Error loading products: {e}")
            self.products = []

    def list_all_products(self):
        """Return all products"""
        return self.products

    def list_by_category(self, category):
        """Return products filtered by category"""
        return [p for p in self.products if p.category.lower() == category.lower()]
    
    def search_products(self, search_term):
        """Search products by name, category, or product ID"""
        search_term = search_term.lower()
        return [p for p in self.products if (
            search_term in p.name.lower() or
            search_term in p.category.lower() or
            search_term in p.product_id.lower()
        )]
    
    def get_product_by_id(self, product_id):
        """Get a specific product by ID"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def get_available_products(self):
        """Return only products that are in stock"""
        return [p for p in self.products if p.stock > 0]
    
    def get_low_stock_products(self, threshold=5):
        """Return products with low stock"""
        return [p for p in self.products if 0 < p.stock <= threshold]
    
    def get_out_of_stock_products(self):
        """Return products that are out of stock"""
        return [p for p in self.products if p.stock == 0]
    
    def get_categories(self):
        """Get unique list of all categories"""
        categories = set()
        for product in self.products:
            categories.add(product.category)
        return sorted(list(categories))
    
    def get_total_products(self):
        """Get total number of products"""
        return len(self.products)
    
    def get_total_value(self):
        """Get total value of all inventory"""
        return sum(p.price * p.stock for p in self.products)
    
    def refresh(self):
        """Reload products from file"""
        self.load_products()

    def __str__(self):
        return f"Catalogue with {len(self.products)} products"
    
    def __repr__(self):
        return self.__str__()