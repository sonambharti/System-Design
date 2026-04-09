# Payment Gateway
A payment gateway is a tool that enables businesses to accept payments online from anywhere via different channels and devices.
It helps in receiving payments from the customers online and acts as a link between their bank account and that of the merchants.
Furthermore, it authorizes a merchant to conduct a payment transaction through payment sources, like net banking, debit card, credit card, and UPI.

#### How does payment gateway works?
A payment gateway supports online payment transactions by securing sensitive information like bank and card details provided by the users.
Here is how it works:
- Once customers place an order on a website or app and clicks ‘Pay Now’, they are redirected to a payment gateway where they enter required details.
- Paytm Payment Gateway then securely sends the card details to the acquiring bank. The issuing bank then receives these details for approval.
- After performing fraud checks, the issuing bank sends the approval or decline message to the acquiring bank.
- The acquiring bank then sends an approval or decline message to the payment gateway.
- If the payment is approved, the acquiring bank accumulates the payment amount from the issuing bank and keeps the funds in the business owner’s merchant account.
- The funds are then transferred to the bank account of the business owner, thus completing the settlement process.

## 🧠 1. Understand the Problem

A payment gateway enables:
👉 User pays → Merchant receives money

**Actors:**
- Customer (payer)
- Merchant (receiver)
- Payment Gateway
- Bank / Card Network (like Visa)


## 📋 2. Requirements

### Functional Requirements
- Process payments (cards, UPI, wallets)
- Authorization & capture
- Refunds
- Payment status tracking

### Non-Functional Requirements
- High availability (99.99%)
- Low latency (<2–3 sec)
- Strong security (PCI-DSS)
- Idempotency (no double charge)


## 🏗️ 3. High-Level Architecture

```
Client → Merchant Server → Payment Gateway → Bank/Card Network
                                   ↓
                             Internal Services
```

### Core Components:
- API Gateway
- Payment Processor
- Fraud Detection
- Ledger System
- Notification Service


## 🔄 4. Payment Flow (Step-by-Step)

### Step 1: Payment Initiation
- User clicks “Pay”
- Merchant sends request to gateway

### Step 2: Tokenization
- Card details → replaced with token (security)

### Step 3: Authorization
- Gateway → acquiring bank → card network → issuing bank
- Bank approves/declines

### Step 4: Capture
- Funds reserved → later captured

### Step 5: Settlement
- Money transferred to merchant account


## 🔑 5. Core APIs
#### Create Payment
```
POST /payments
{ amount, currency, method }
```

#### Check Status
```
GET /payments/{id}
```

#### Refund
```
POST /refunds
```


## 🧩 6. Database Design
#### Payments Table

| id | user_id | amount | status | created_at |

#### Transactions Table

| id | payment_id | type | status |

#### Ledger Table (VERY IMPORTANT)

Tracks money movement:
| account | debit | credit | balance |

👉 Ensures **no money is lost**


## ⚡ 7. Idempotency (Critical)

Problem:
- User clicks “Pay” twice → double charge

Solution:
- Use idempotency key
  ```
  POST /payments (idempotency_key)
  ```
  Same key → same result


## 🔐 8. Security Layer
Must-have:
- Encryption (TLS)
- Tokenization (no raw card storage)
- PCI-DSS compliance
- Fraud detection

Example:
- Velocity checks
- Geo mismatch
- Suspicious patterns


## 🚀 9. Scaling the System 
1. Stateless APIs
    - Horizontally scalable
2. Queue-Based Processing
   Use Apache Kafka:
    - Payment events
    - Retry handling
    - Async workflows
3. Caching
   Use Redis:
    - Payment status
    - Session data


## 🔄 10. Fault Tolerance
#### Problems:
- Bank timeout
- Network failure

#### Solutions:
- Retry with backoff
- Circuit breaker
- Store intermediate states

  
## 🧾 11. Double Entry Ledger System

Every transaction:
```
User Account  → Debit
Merchant Account → Credit
```
This guarantees:
- Consistency
- Auditability


## 🌍 12. Multi-Payment Methods

Support:
- Cards (Visa, Mastercard)
- UPI (India-specific)
- Wallets

Each has:
- Different flows
- Same unified interface


## 📊 13. Observability

Track:
- Success rate
- Latency
- Failure reasons

Use logs + metrics + alerts


## 🧱 14. Final Architecture (Scaled)
```
                ┌──────────────┐
                │ Load Balancer │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ API Gateway  │
                └──────┬───────┘
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
 Payment Service   Fraud Service   Ledger Service
       ↓               ↓               ↓
     Queue (Kafka)     ↓          Database Cluster
       ↓
 External Banks / Networks
```


## ⚖️ 15. Key Tradeoffs
```
| Decision           | Pros           | Cons       |
| ------------------ | -------------- | ---------- |
| Sync vs Async      | Faster UX      | Complexity |
| Strong consistency | Safe money ops | Slower     |
| Tokenization       | Secure         | Extra step |

```


## 🧠 16. Interview Tips

When explaining:
1. Start with flow
2. Add idempotency
3. Highlight ledger system
4. Discuss failures & retries
5. Emphasize security


## 🧾 Final Summary

A payment gateway must:
- Be extremely reliable
- Prevent double charging
- Maintain accurate ledger
- Handle failures gracefully
- Scale to millions of transactions
