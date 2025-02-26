#  Token Bucket Algorithm

##  What is the Token Bucket Algorithm?
The Token Bucket Algorithm is a rate-limiting algorithm used to control the number of requests processed over time. <br/>
It allows occasional bursts of requests while ensuring a steady rate of processing.

##  How Does It Work?
A bucket holds a fixed number of tokens (e.g., max_tokens = 5). <br/>
Tokens are refilled at a constant rate (e.g., refill_rate = 1 token per second). <br/>
Every request consumes one token. <br/>
  -  If the bucket is empty, requests are rejected or delayed.
  -  If the bucket is full, extra tokens are discarded.
    
###  Key Properties
✅ Supports bursts (as long as tokens are available). <br/>
✅ Enforces a steady rate (tokens refill at a constant speed). <br/>
✅ Simple to implement with minimal computation. <br/>


###  Explanation of the Token Bucket Algorithm Implementation

1. Refilling Tokens Dynamically (_refill_tokens)
  -  Time-based token refill → Tokens are replenished based on elapsed time since last request.
  -  Prevents overflows → min(self.max_tokens, self.tokens + new_tokens) ensures the bucket never exceeds its capacity.
2. Allowing or Denying Requests (allow_request)
  -  Refills tokens before checking availability → Ensures fairness in request handling.
  -  If tokens are available, deduct one and allow the request.
  -  If no tokens are available, reject the request.
3. Handling Bursts
  -  If tokens are available, multiple requests can be served instantly.
  -  If all tokens are used up, the system enforces a strict rate limit.

###  How the Token Bucket Algorithm Prevents API Abuse

✅ Controls Request Rate → Ensures no more than X requests per second. <br/>
✅ Prevents Sudden Overload → Rejects excessive requests, preventing server crashes. <br/>
✅ Allows Temporary Bursts → Clients with occasional high traffic are not penalized. <br/>
✅ Protects Against DDoS → Blocks abusive clients exceeding their allowed rate. <br/>

Example: <br/>
  -  If an API allows 10 requests per second, a client can’t exceed this rate.
  -  If a bot sends 100 requests in 1 second, only 10 are allowed, and the rest are dropped.

#  Alternatives to Token Bucket Algorithm

1. Sliding Window Counter
&nbsp;&nbsp;&nbsp;
##  How It Works:
&nbsp;&nbsp;&nbsp;
  -  Maintains a fixed time window (e.g., 1 minute) and counts the number of requests.
&nbsp;&nbsp;&nbsp;
  -  If the request count exceeds the limit, new requests are rejected.
&nbsp;&nbsp;&nbsp;
  -  Instead of resetting at fixed intervals, the window slides forward to count recent requests. <br/>
&nbsp;&nbsp;&nbsp;

✅ Pros <br/>
&nbsp;&nbsp;&nbsp;
✔ Ensures a strict rate limit (e.g., 100 requests per minute). <br/>
&nbsp;&nbsp;&nbsp;
✔ Smooth request distribution over time. <br/>
&nbsp;&nbsp;&nbsp;

❌ Cons <br/>
&nbsp;&nbsp;&nbsp;
✖ Doesn’t support burst handling well. <br/>
&nbsp;&nbsp;&nbsp;
✖ Slightly higher memory usage (stores timestamps of requests). <br/>



🔹 Use Case: User authentication attempts (e.g., login rate limits). <br/>

2. Leaky Bucket Algorithm
&nbsp;&nbsp;&nbsp;
##  How It Works:
&nbsp;&nbsp;&nbsp;
A queue (bucket) stores incoming requests. <br/>
Requests are processed at a constant rate. <br/>
If the queue overflows, new requests are dropped. <br/>
&nbsp;&nbsp;&nbsp;

✅ Pros <br/>
&nbsp;&nbsp;&nbsp;
✔ Enforces a steady, predictable request rate. <br/>
&nbsp;&nbsp;&nbsp;
✔ Prevents server overload with a fixed processing rate. <br/>

&nbsp;&nbsp;&nbsp;
❌ Cons <br/>
&nbsp;&nbsp;&nbsp;
✖ Can cause delays → Requests are queued instead of instantly processed. <br/>
&nbsp;&nbsp;&nbsp;
✖ No burst handling → Extra requests are discarded, not stored. <br/>


🔹 Use Case: Network traffic shaping, preventing congestion in routers. <br/>

##  When to Use Each Algorithm?

-    Token Bucket → Best for API Rate Limiting (allows bursts + smooth limits).
-    Sliding Window Counter → Best for User Authentication Rate Limits (strict limit).
-    Leaky Bucket → Best for Network Traffic Shaping (ensures steady processing).


##  Final Thoughts

-  Token Bucket is widely used in API rate limiting (e.g., AWS, Cloudflare).
-  Sliding Window works best for authentication systems.
-  Leaky Bucket ensures constant processing speed in network systems.


#  Real-World Example of Token Bucket Rate Limiting in Cloud Services

##  How Cloud Services Use Token Bucket Rate Limiting
Cloud platforms like AWS, Google Cloud, Cloudflare, and API gateways implement Token Bucket rate limiting <br/>
to control API requests from users or services.

###  Example 1: AWS API Gateway Rate Limiting
AWS API Gateway allows you to set two limits:

1.  Burst Capacity (Token Bucket size) → Allows a temporary high number of requests.
2.  Steady Rate (Refill Rate per second) → Ensures long-term rate control.

###  How It Works in AWS?

-  Suppose an API is configured with:
    -  100 requests burst capacity (bucket size)
    -  10 requests per second refill rate
-  A user can instantly send 100 requests (if the bucket is full).
-  After using all tokens, they can only send 10 requests per second.
-  Excess requests are throttled (HTTP 429 Too Many Requests).

<br/>
✅ Allows temporary spikes in traffic. <br/>
✅ Ensures fairness for all users. <br/>
✅ Prevents overloading backend servers. <br/>

###  Example 2: Cloudflare API Rate Limiting
Cloudflare protects web applications from abuse by enforcing rate limits on:
-  Login attempts (prevents brute-force attacks).
-  DDoS protection (blocks bots sending millions of requests).
<br/>
Cloudflare's Token Bucket Example
-  Configured for 50 requests per minute (bucket size = 50).
-  Refill rate 10 requests per 10 seconds.
-  If a bot sends 100 requests in 1 minute:
    -  First 50 are accepted.
    -  Next 50 are blocked (429 Error).
<br/>
<br/>
✅ Allows normal user behavior but blocks abuse. <br/>
✅ Reduces server costs and improves security.
<br/>

###  Example 3: Google Cloud Functions Rate Limiting

Google Cloud Functions use Token Bucket for API calls.
-  If a function is limited to 500 requests per second:
    -  Can handle short bursts of traffic (e.g., a sudden spike from 200 users).
    -  But if requests exceed the bucket size, it queues or drops them.
<br/>
✅ Prevents unexpected overload on cloud functions. <br/>
✅ Ensures fair resource allocation across users.

<br/>
##  Real-World Impact of Token Bucket

🔹 Netflix & YouTube → Control video streaming API requests. <br/>
🔹 Facebook & Instagram → Prevent spam bots from overloading their servers. <br/>
🔹 Stripe & PayPal → Enforce API limits on payment processing requests. <br/>
🔹 ChatGPT API → Uses rate limits to prevent excessive usage per user. <br/>
