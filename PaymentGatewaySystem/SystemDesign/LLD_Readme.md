# Low Level Design 

## 🧠 1. Key Design Goals

We want:
- Extensible payment methods (Card, UPI, Wallet)
- Secure processing
- Idempotency
- Clear separation of concerns
- Easy to scale & modify


## 🏗️ 2. High-Level Class Breakdown
### Core Entities
- `Payment`
- `Transaction`
- `User`
- `Merchant`

### Services
- `PaymentService`
- `PaymentProcessor`
- `FraudService`
- `LedgerService`

### Payment Methods
- CardPayment
- UPIPayment
-  WalletPayment


## 🎯 3. Design Patterns Used

| Pattern                     | Where Used              | Why                            |
| --------------------------- | ----------------------- | ------------------------------ |
| **Strategy**                | Payment methods         | Switch between Card/UPI/Wallet |
| **Factory**                 | Payment method creation | Decouple object creation       |
| **Singleton**               | PaymentGateway          | Single orchestrator            |
| **Chain of Responsibility** | Fraud checks            | Multiple validations           |
| **Observer**                | Notifications           | Decouple event handling        |
| **Decorator (optional)**    | Logging/retry           | Add behavior dynamically       |


## 🧩 4. Python Implementation
### 🔹 Enums & Models
```
from enum import Enum
import uuid
from abc import ABC, abstractmethod

class PaymentStatus(Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    FAILED = "FAILED"
    CAPTURED = "CAPTURED"

class Payment:
    def __init__(self, user_id, amount, method):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.amount = amount
        self.method = method
        self.status = PaymentStatus.CREATED
```

### 🔹 Strategy Pattern (Payment Methods)
```
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, payment: Payment):
        pass


class CardPayment(PaymentStrategy):
    def pay(self, payment):
        print("Processing Card Payment")
        return True


class UPIPayment(PaymentStrategy):
    def pay(self, payment):
        print("Processing UPI Payment")
        return True


class WalletPayment(PaymentStrategy):
    def pay(self, payment):
        print("Processing Wallet Payment")
        return True
```

### 🔹 Factory Pattern
```
class PaymentFactory:
    @staticmethod
    def get_payment_method(method):
        if method == "CARD":
            return CardPayment()
        elif method == "UPI":
            return UPIPayment()
        elif method == "WALLET":
            return WalletPayment()
        else:
            raise Exception("Invalid payment method")
```

### 🔹 Chain of Responsibility (Fraud Checks)

```
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
            raise Exception("High risk transaction")
        return super().check(payment)


class VelocityCheck(FraudCheck):
    def check(self, payment):
        print("Velocity check passed")
        return super().check(payment)
```

### 🔹 Observer Pattern (Notifications)

```
class Observer(ABC):
    @abstractmethod
    def update(self, payment):
        pass


class EmailNotifier(Observer):
    def update(self, payment):
        print(f"Email sent for payment {payment.id}")


class SMSNotifier(Observer):
    def update(self, payment):
        print(f"SMS sent for payment {payment.id}")
```

### 🔹 Ledger Service

```
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
        print("Ledger updated")
```

### 🔹 Singleton Payment Gateway

```
class PaymentGateway:
    _instance = None

    def __init__(self):
        self.observers = []
        self.ledger = LedgerService()

        # Fraud chain
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

    def process_payment(self, payment: Payment):
        try:
            # Fraud check
            self.fraud_chain.check(payment)

            # Strategy selection
            strategy = PaymentFactory.get_payment_method(payment.method)

            success = strategy.pay(payment)

            if success:
                payment.status = PaymentStatus.AUTHORIZED
                self.ledger.record(payment)
                self.notify(payment)
                return payment
            else:
                payment.status = PaymentStatus.FAILED
                return payment

        except Exception as e:
            payment.status = PaymentStatus.FAILED
            print("Payment Failed:", str(e))
            return payment
```

### 🔹 Payment Service (Facade Layer)

```
class PaymentService:
    def __init__(self):
        self.gateway = PaymentGateway.get_instance()

    def create_payment(self, user_id, amount, method):
        payment = Payment(user_id, amount, method)
        return self.gateway.process_payment(payment)
```

### Usage Example
```
if __name__ == "__main__":
    service = PaymentService()

    gateway = PaymentGateway.get_instance()
    gateway.register_observer(EmailNotifier())
    gateway.register_observer(SMSNotifier())

    payment = service.create_payment(
        user_id="user123",
        amount=500,
        method="CARD"
    )

    print("Final Status:", payment.status)
```


## 🔄 5. Flow Explained
1. User calls PaymentService
2. Payment created
3. Fraud checks executed (Chain)
4. Strategy selected (Factory + Strategy)
5. Payment processed
6. Ledger updated
7. Observers notified


## ⚡ 6. Why This Design Works

### ✅ Extensible
Add new method:
```
class CryptoPayment(PaymentStrategy):
    ...
```
No change elsewhere ✅

### ✅ Scalable
- Services are loosely coupled
- Easy to split into microservices

### ✅ Safe
- Fraud checks
- Ledger tracking

  
## 🧾 7. Summary of Patterns
- Strategy → Payment methods
- Factory → Object creation
- Singleton → Gateway instance
- Observer → Notifications
- Chain of Responsibility → Fraud checks
- Facade → PaymentService
