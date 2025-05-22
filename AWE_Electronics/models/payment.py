def choose_payment_method():
    print("\n Payment Methods:")
    print("1. PayPal")
    print("2. Credit Card")
    choice = input("Choose payment method (1 or 2): ")

    if choice == "1":
        email = input("Enter PayPal Email: ")
        return f"PayPal - {email}"
    elif choice == "2":
        name = input("Cardholder Name: ")
        return f"Credit Card - {name}"
    else:
        print("Invalid choice, using Cash as fallback.")
        return "Cash"
