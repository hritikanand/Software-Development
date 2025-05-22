from models.catalogue import Catalogue

def browse_products():
    cat = Catalogue()
    print("\n All Products:")
    for product in cat.list_all_products():
        print(product)

def filter_by_category():
    cat = Catalogue()
    category = input("Enter category to filter: ")
    results = cat.list_by_category(category)
    if results:
        print(f"\n Products in '{category}':")
        for product in results:
            print(product)
    else:
        print(" No products found in that category.")
