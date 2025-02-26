#  Doubly Linked List + HashMap Approach (O(1) Solution)
class Node:
    """A node in the doubly linked list."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """LRU Cache using Doubly Linked List + HashMap."""
    def __init__(self, capacity):
        self.cache = {}  # Maps key -> Node
        self.capacity = capacity
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head  # Establish head-tail link

    def _remove(self, node):
        """Removes a node from the doubly linked list."""
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add_to_end(self, node):
        """Adds a node to the end of the doubly linked list (most recent)."""
        prev, nxt = self.tail.prev, self.tail
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key):
        """Retrieve key and move to most recently used."""
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_end(node)
        return node.value

    def put(self, key, value):
        """Insert or update key and maintain LRU property."""
        if key in self.cache:
            self._remove(self.cache[key])  # Remove existing node

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_end(node)

        if len(self.cache) > self.capacity:
            lru = self.head.next  # LRU is at the front
            self._remove(lru)
            del self.cache[lru.key]  # Remove from dict

# Usage
lru = LRUCache(2)
lru.put(1, "A")
lru.put(2, "B")
print(lru.get(1))  # Output: "A"
lru.put(3, "C")  # Evicts key 2
print(lru.get(2))  # Output: -1 (not found)
