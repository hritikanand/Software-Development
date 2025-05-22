# models/catalogue.py
from utils.file_handler import read_json
from models.product import Product

PRODUCT_FILE = "data/products.json"

class Catalogue:
    def __init__(self):
        self.products = [Product(**prod) for prod in read_json(PRODUCT_FILE)]

    def list_all_products(self):
        return self.products

    def list_by_category(self, category):
        return [p for p in self.products if p.category.lower() == category.lower()]
