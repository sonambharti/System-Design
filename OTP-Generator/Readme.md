# Design of a Basic OTP System
A One-Time Password (OTP) system generates a temporary passcode that is valid for a short duration or a <br>
single authentication session. It is widely used in multi-factor authentication (MFA) to enhance security.

## Components of an OTP System

1. User Registration & Identity Verification: <br>
    -  A user registers their phone number or email. <br>
    -  The system stores this securely. <br>
2. OTP Generation:<br>
    -  The server generates a random numeric or alphanumeric OTP. <br>
    -  The OTP length is usually 4-8 characters. <br>
    -  The OTP is timestamped to enforce expiration. <br>
3. OTP Delivery:<br>
    -  The OTP is sent via SMS, Email, or an Authenticator App. <br>
4. OTP Validation:<br>
    -  The user inputs the OTP. <br>
    -  The system verifies the OTP, expiry time, and match. <br>
    -  If valid, authentication succeeds; otherwise, it fails. <br>
5. Security Measures:<br>
    -  OTPs should be unique for each request. <br>
    -  Rate limiting prevents brute force attacks. <br>
    -  Expiration time prevents reuse. <br>


## How It Works
1. The system generates a 6-digit OTP and stores it with a timestamp.
2. It prints the OTP (in a real system, this would be sent via email/SMS).
3. The user enters the OTP, which is then validated:
   -  If expired, authentication fails. <br>
   -  If incorrect, authentication fails. <br>
   -  If correct, authentication succeeds, and OTP is removed. <br>


## Enhancements for Production
1. Secure Storage: Use Redis instead of an in-memory dictionary for storing OTPs.
2. Send OTP via SMS/Email: Integrate an SMS gateway (Twilio, AWS SNS) or email service.
3. Rate Limiting: Prevent multiple OTP requests in a short period.
4. Hashing OTPs: Store OTPs securely using hashing instead of plaintext.
