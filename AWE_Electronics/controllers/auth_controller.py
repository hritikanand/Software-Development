from utils.file_handler import read_json, write_json
from models.customer import Customer

USER_FILE = "data/users.json"

def register_customer():
    users = read_json(USER_FILE)
    username = input("Enter username: ")
    if any(u['username'] == username for u in users):
        print(" Username already exists.")
        return

    password = input("Enter password: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")

    new_customer = Customer(username, password, email, address, phone)
    users.append(new_customer.to_dict())
    write_json(USER_FILE, users)
    print(" Customer registered successfully!")

def login():
    users = read_json(USER_FILE)
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f" Welcome, {username}!")
            return user
    print(" Login failed.")
    return None
