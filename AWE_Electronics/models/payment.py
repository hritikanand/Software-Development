def choose_payment_method():
    """Choose payment method from command line (for CLI version)"""
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

class Payment:
    """Payment model for managing payment information"""
    
    def __init__(self, method, account_holder, amount, currency="AUD"):
        self.method = method  # PayPal, Credit Card, etc.
        self.account_holder = account_holder
        self.amount = float(amount)
        self.currency = currency
        self.status = "Pending"
        self.transaction_id = None
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            "method": self.method,
            "account_holder": self.account_holder,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "transaction_id": self.transaction_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Payment instance from dictionary"""
        payment = cls(
            method=data.get("method", ""),
            account_holder=data.get("account_holder", ""),
            amount=data.get("amount", 0.0),
            currency=data.get("currency", "AUD")
        )
        payment.status = data.get("status", "Pending")
        payment.transaction_id = data.get("transaction_id")
        return payment
    
    def process_payment(self):
        """Process the payment (simulation)"""
        # In a real system, this would integrate with payment gateways
        import uuid
        
        if self.amount <= 0:
            self.status = "Failed"
            return False
        
        # Simulate payment processing
        self.transaction_id = str(uuid.uuid4())[:16].upper()
        self.status = "Completed"
        return True
    
    def refund(self, amount=None):
        """Process refund (simulation)"""
        if self.status != "Completed":
            return False
        
        refund_amount = amount if amount else self.amount
        if refund_amount > self.amount:
            return False
        
        self.status = "Refunded"
        return True
    
    def validate(self):
        """Validate payment information"""
        errors = []
        
        if not self.method:
            errors.append("Payment method is required")
        
        if not self.account_holder or len(self.account_holder.strip()) < 2:
            errors.append("Account holder name is required")
        
        if self.amount <= 0:
            errors.append("Payment amount must be greater than zero")
        
        return errors
    
    def get_display_method(self):
        """Get formatted payment method for display"""
        return f"{self.method} - {self.account_holder}"
    
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == "Completed"
    
    def __str__(self):
        return f"{self.method} payment of {self.currency} {self.amount:.2f} by {self.account_holder} - {self.status}"
    
    def __repr__(self):
        return f"Payment(method='{self.method}', amount={self.amount}, status='{self.status}')"