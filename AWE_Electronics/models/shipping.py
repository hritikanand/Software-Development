def collect_shipping_details():
    print("\n📦 Enter Shipping Details:")
    name = input("Full Name: ")
    address = input("Address: ")
    phone = input("Phone Number: ")

    return {
        "name": name,
        "address": address,
        "phone": phone
    }
