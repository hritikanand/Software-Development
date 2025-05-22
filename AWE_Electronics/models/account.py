class Account:
    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password  # Simple plain text for now (hash in future)
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role
        }
