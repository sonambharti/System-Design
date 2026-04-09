'''
1. What This Application Covers

✔ Create payment
✔ Prevent duplicate payments (idempotency)
✔ Process via Card / UPI / Wallet
✔ Fraud detection
✔ Ledger tracking
✔ Notifications
✔ Refund support

2. Payment Flow
- Request hits PaymentService
- Idempotency check
- Payment object created
- Fraud checks run
- Strategy selected (Card/UPI/etc.)
- Payment processed
- Ledger updated
- Notifications sent
- Stored in DB
'''


import uuid
import time
from enum import Enum
from abc import ABC, abstractmethod

# ===================== ENUMS =====================

class PaymentStatus(Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

# ===================== DATABASE (IN-MEMORY) =====================

class InMemoryDB:
    payments = {}
    idempotency_keys = {}

# ===================== MODELS =====================

class Payment:
    def __init__(self, user_id, amount, method, idempotency_key):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.amount = amount
        self.method = method
        self.status = PaymentStatus.CREATED
        self.idempotency_key = idempotency_key
        self.created_at = time.time()

# ===================== STRATEGY =====================

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, payment):
        pass


class CardPayment(PaymentStrategy):
    def pay(self, payment):
        print("💳 Processing Card Payment...")
        return True


class UPIPayment(PaymentStrategy):
    def pay(self, payment):
        print("📱 Processing UPI Payment...")
        return True


class WalletPayment(PaymentStrategy):
    def pay(self, payment):
        print("👛 Processing Wallet Payment...")
        return True

# ===================== FACTORY =====================

class PaymentFactory:
    @staticmethod
    def get_strategy(method):
        if method == "CARD":
            return CardPayment()
        elif method == "UPI":
            return UPIPayment()
        elif method == "WALLET":
            return WalletPayment()
        else:
            raise Exception("Invalid payment method")

# ===================== FRAUD (CHAIN OF RESPONSIBILITY) =====================

class FraudCheck(ABC):
    def __init__(self, next_check=None):
        self.next_check = next_check

    def check(self, payment):
        if self.next_check:
            return self.next_check.check(payment)
        return True


class AmountCheck(FraudCheck):
    def check(self, payment):
        if payment.amount > 100000:
            raise Exception("❌ High-risk transaction blocked")
        return super().check(payment)


class VelocityCheck(FraudCheck):
    def check(self, payment):
        print("✅ Velocity check passed")
        return super().check(payment)

# ===================== OBSERVER =====================

class Observer(ABC):
    @abstractmethod
    def update(self, payment):
        pass


class EmailNotifier(Observer):
    def update(self, payment):
        print(f"📧 Email: Payment {payment.id} is {payment.status.value}")


class SMSNotifier(Observer):
    def update(self, payment):
        print(f"📩 SMS: Payment {payment.id} is {payment.status.value}")

# ===================== LEDGER =====================

class LedgerService:
    def __init__(self):
        self.entries = []

    def record(self, payment):
        entry = {
            "payment_id": payment.id,
            "amount": payment.amount,
            "status": payment.status.value
        }
        self.entries.append(entry)
        print("📒 Ledger updated")

# ===================== PAYMENT GATEWAY (SINGLETON) =====================

class PaymentGateway:
    _instance = None

    def __init__(self):
        self.observers = []
        self.ledger = LedgerService()
        self.fraud_chain = AmountCheck(VelocityCheck())

    @staticmethod
    def get_instance():
        if not PaymentGateway._instance:
            PaymentGateway._instance = PaymentGateway()
        return PaymentGateway._instance

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify(self, payment):
        for obs in self.observers:
            obs.update(payment)

    def process_payment(self, payment):
        try:
            # Fraud check
            self.fraud_chain.check(payment)

            # Strategy
            strategy = PaymentFactory.get_strategy(payment.method)
            success = strategy.pay(payment)

            if success:
                payment.status = PaymentStatus.AUTHORIZED
                self.ledger.record(payment)
                self.notify(payment)
            else:
                payment.status = PaymentStatus.FAILED

        except Exception as e:
            payment.status = PaymentStatus.FAILED
            print(e)

        return payment

# ===================== SERVICE LAYER =====================

class PaymentService:
    def __init__(self):
        self.gateway = PaymentGateway.get_instance()

    def create_payment(self, user_id, amount, method, idempotency_key):
        # Idempotency check
        if idempotency_key in InMemoryDB.idempotency_keys:
            print("⚠️ Duplicate request detected")
            return InMemoryDB.idempotency_keys[idempotency_key]

        payment = Payment(user_id, amount, method, idempotency_key)

        processed_payment = self.gateway.process_payment(payment)

        # Save
        InMemoryDB.payments[payment.id] = processed_payment
        InMemoryDB.idempotency_keys[idempotency_key] = processed_payment

        return processed_payment

    def get_payment(self, payment_id):
        return InMemoryDB.payments.get(payment_id)

    def refund_payment(self, payment_id):
        payment = self.get_payment(payment_id)

        if not payment:
            raise Exception("Payment not found")

        if payment.status != PaymentStatus.AUTHORIZED:
            raise Exception("Only authorized payments can be refunded")

        payment.status = PaymentStatus.REFUNDED
        print("💸 Refund processed")

        return payment

# ===================== APPLICATION =====================

if __name__ == "__main__":
    service = PaymentService()
    gateway = PaymentGateway.get_instance()

    # Register observers
    gateway.register_observer(EmailNotifier())
    gateway.register_observer(SMSNotifier())

    print("\n=== PAYMENT 1 ===")
    p1 = service.create_payment(
        user_id="user1",
        amount=500,
        method="CARD",
        idempotency_key="abc123"
    )

    print("\n=== DUPLICATE PAYMENT (IDEMPOTENCY) ===")
    p2 = service.create_payment(
        user_id="user1",
        amount=500,
        method="CARD",
        idempotency_key="abc123"
    )

    print("\n=== PAYMENT 2 ===")
    p3 = service.create_payment(
        user_id="user2",
        amount=2000,
        method="UPI",
        idempotency_key="xyz789"
    )

    print("\n=== REFUND ===")
    service.refund_payment(p1.id)

    print("\n=== FINAL STATE ===")
    print(InMemoryDB.payments)
