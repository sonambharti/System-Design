"""
# Implement Least Recently Used (LRU) Cache using Ordered Dict

Key Concept: Store frequently used data with automatic eviction.
Use Case: Optimizing slow database queries.
"""

from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()  # Maintains insertion order
        self.capacity = capacity

    def get(self, key: int) -> int:
        """Retrieve the value of the key and move it to the end (most recently used)."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """Insert or update key, and move it to the end (most recently used)."""
        if key in self.cache:
            self.cache.move_to_end(key)  # Move to end if already exists
        self.cache[key] = value  
        
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove least recently used item

# Usage
lru = LRUCache(2)
lru.put(1, "A")
lru.put(2, "B")
print(lru.get(1))  # Output: "A"
lru.put(3, "C")  # Evicts key 2
print(lru.get(2))  # Output: -1 (not found)
