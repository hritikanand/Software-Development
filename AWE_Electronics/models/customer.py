from models.account import Account

class Customer(Account):
    def __init__(self, username, password, email, address, phone_number):
        super().__init__(username, password, email, "customer")
        self.address = address
        self.phone_number = phone_number
        self.cart = []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "address": self.address,
            "phone_number": self.phone_number,
            "cart": self.cart
        })
        return data
