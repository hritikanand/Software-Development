def collect_shipping_details():
    """Collect shipping details from command line (for CLI version)"""
    print("\n📦 Enter Shipping Details:")
    name = input("Full Name: ")
    address = input("Address: ")
    phone = input("Phone Number: ")

    return {
        "name": name,
        "address": address,
        "phone": phone
    }

class Shipping:
    """Shipping model for managing delivery information"""
    
    def __init__(self, name, address, phone, city="", state="", postal_code="", country="Australia"):
        self.name = name
        self.address = address
        self.phone = phone
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
    
    def to_dict(self):
        """Convert shipping info to dictionary"""
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Shipping instance from dictionary"""
        return cls(
            name=data.get("name", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            city=data.get("city", ""),
            state=data.get("state", ""),
            postal_code=data.get("postal_code", ""),
            country=data.get("country", "Australia")
        )
    
    def validate(self):
        """Validate shipping information"""
        errors = []
        
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Name is required")
        
        if not self.address or len(self.address.strip()) < 5:
            errors.append("Address is required")
        
        if not self.phone or len(self.phone.strip()) < 10:
            errors.append("Valid phone number is required")
        
        return errors
    
    def get_formatted_address(self):
        """Get formatted address string"""
        parts = [self.address]
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.country:
            parts.append(self.country)
        
        return ", ".join(filter(None, parts))
    
    def __str__(self):
        return f"Shipping to {self.name} at {self.get_formatted_address()}"
    
    def __repr__(self):
        return f"Shipping(name='{self.name}', address='{self.address}', phone='{self.phone}')"