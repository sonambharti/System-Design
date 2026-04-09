""" 
# Python Implementation of a Simple Payment Gateway

Customer → Merchant → Payment Gateway → Acquiring Bank → Card Network → Issuing Bank
                    ← Payment Status  ←  ←  ←  ←  ←
"""

import hashlib
import secrets
import time

class PaymentGateway:
    def __init__(self):
        self.transactions = {}  # Store transactions

    def encrypt_card_details(self, card_number):
        """Encrypt the card number using SHA-256 hashing (mock encryption)."""
        return hashlib.sha256(card_number.encode()).hexdigest()

    def process_payment(self, merchant_id, card_number, expiry, cvv, amount):
        """Simulate a payment processing system."""
        # Encrypt card details
        encrypted_card = self.encrypt_card_details(card_number)
        
        # Generate transaction ID
        transaction_id = secrets.token_hex(8)
        
        # Mock bank verification (simplified)
        if not self.verify_bank(encrypted_card, expiry, cvv, amount):
            return {"status": "Failed", "message": "Payment Declined", "transaction_id": transaction_id}
        
        # Store transaction details
        self.transactions[transaction_id] = {
            "merchant_id": merchant_id,
            "amount": amount,
            "status": "Success",
            "timestamp": time.time(),
        }
        
        return {"status": "Success", "message": "Payment Approved", "transaction_id": transaction_id}

    def verify_bank(self, encrypted_card, expiry, cvv, amount):
        """Mock bank verification logic."""
        # Simulate bank verification by checking basic conditions
        if len(expiry) != 5 or len(cvv) != 3:
            return False
        if amount <= 0:
            return False
        return True  # Assuming transaction is approved for valid inputs

    def check_transaction_status(self, transaction_id):
        """Check the status of a transaction."""
        return self.transactions.get(transaction_id, {"status": "Not Found", "message": "Invalid Transaction ID"})

# Usage Example
gateway = PaymentGateway()
merchant_id = "Amazon123"

# Step 1: Customer enters payment details
card_number = "4111111111111111"  # Mock Visa card number
expiry = "12/25"  # MM/YY format
cvv = "123"
amount = 500.00

# Step 2: Process Payment
payment_response = gateway.process_payment(merchant_id, card_number, expiry, cvv, amount)
print(payment_response)

# Step 3: Check Transaction Status
transaction_id = payment_response["transaction_id"]
status = gateway.check_transaction_status(transaction_id)
print(status)
