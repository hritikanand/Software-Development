from controllers.auth_controller import register_customer, login
from controllers.product_controller import browse_products, filter_by_category
from controllers.cart_controller import add_to_cart, view_cart
from controllers.order_controller import checkout
from controllers.admin_controller import (
    view_products, add_product, update_stock,
    delete_product, generate_sales_report
)

def customer_menu(user):
    while True:
        print("\n--- Customer Menu ---")
        print("1. Browse All Products")
        print("2. Filter Products by Category")
        print("3. Add Product to Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            browse_products()
        elif choice == "2":
            filter_by_category()
        elif choice == "3":
            add_to_cart(user)
        elif choice == "4":
            view_cart(user)
        elif choice == "5":
            checkout(user)
        elif choice == "6":
            print("👋 Logged out.\n")
            break
        else:
            print(" Invalid choice. Please try again.")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Products")
        print("2. Add New Product")
        print("3. Update Product Stock")
        print("4. Delete Product")
        print("5. Generate Sales Report")
        print("6. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            generate_sales_report()
        elif choice == "6":
            print("👋 Logged out.\n")
            break
        else:
            print(" Invalid option.")

def main_menu():
    user = None
    while True:
        if user:
            if user.get("role") == "customer":
                customer_menu(user)
            elif user.get("role") == "admin":
                admin_menu()
            user = None  # Reset after logout
            continue

        print("\n==== AWE Electronics Store ====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            register_customer()
        elif choice == "2":
            user = login()
            if user:
                print(f" Logged in as {user['role']}")
        elif choice == "3":
            print(" Goodbye!")
            break
        else:
            print(" Invalid option. Please select 1, 2 or 3.")

if __name__ == "__main__":
    main_menu()
