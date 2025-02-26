"""
# Implement a Rate Limiter (Token Bucket Algorithm)

Key Concept: Controls the number of requests a user can make within a given time window.
Use Case: Preventing API abuse.
"""

import time
from collections import deque

class TokenBucketRateLimiter:
    def __init__(self, max_tokens, refill_rate):
        self.max_tokens = max_tokens  # Maximum tokens (requests) allowed
        self.refill_rate = refill_rate  # Tokens refilled per second
        self.tokens = max_tokens  # Start with full tokens
        self.last_refill_time = time.time()

    def _refill_tokens(self):
        """Refills tokens based on elapsed time since last refill."""
        now = time.time()
        elapsed_time = now - self.last_refill_time
        new_tokens = elapsed_time * self.refill_rate
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
        self.last_refill_time = now

    def allow_request(self):
        """Returns True if request is allowed, otherwise False."""
        self._refill_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

# Usage
limiter = TokenBucketRateLimiter(max_tokens=5, refill_rate=1)  # 5 requests allowed per second
for _ in range(10):
    print("Request allowed:", limiter.allow_request())
    time.sleep(0.3)  # Simulating requests at different intervals
