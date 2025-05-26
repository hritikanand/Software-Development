class Account:
    """Base account class for all user types"""
    
    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password  # In production, this should be hashed
        self.email = email
        self.role = role

    def to_dict(self):
        """Convert account to dictionary for JSON storage"""
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role
        }
    
    def __str__(self):
        return f"Account(username={self.username}, role={self.role})"
    
    def __repr__(self):
        return self.__str__()