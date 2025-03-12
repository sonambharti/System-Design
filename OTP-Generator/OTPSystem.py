"""
design of a basic OTP system and implement it.
"""
import random
import time

class OTPSystem:
    def __init__(self, otp_length=6, expiry_time=60):
        self.otp_length = otp_length
        self.expiry_time = expiry_time  # OTP valid duration in seconds
        self.otp_store = {}  # Store OTPs temporarily

    def generate_otp(self, user_id):
        """Generate and store an OTP for a user."""
        otp = ''.join(str(random.randint(0, 9)) for _ in range(self.otp_length))
        self.otp_store[user_id] = {'otp': otp, 'timestamp': time.time()}
        print(f"OTP for {user_id}: {otp} (Valid for {self.expiry_time} seconds)")  # Mock sending
        return otp

    def validate_otp(self, user_id, user_otp):
        """Validate the entered OTP."""
        if user_id not in self.otp_store:
            return "Invalid request: No OTP generated."

        stored_otp_data = self.otp_store[user_id]
        if time.time() - stored_otp_data['timestamp'] > self.expiry_time:
            del self.otp_store[user_id]  # Remove expired OTP
            return "OTP expired."

        if stored_otp_data['otp'] == user_otp:
            del self.otp_store[user_id]  # Remove OTP after successful validation
            return "OTP verified successfully."
        return "Invalid OTP."

# Usage Example
otp_system = OTPSystem()
user_id = "user@example.com"

# Step 1: Generate OTP
otp_system.generate_otp(user_id)

# Simulate User Input
user_input = input("Enter OTP: ")

# Step 2: Validate OTP
print(otp_system.validate_otp(user_id, user_input))
