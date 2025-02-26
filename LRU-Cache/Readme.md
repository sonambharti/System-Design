# Least Recently Used (LRU) Cache

## What is LRU Cache?

An LRU (Least Recently Used) Cache is a data structure that stores frequently accessed data but automatically </br>
removes the least recently used items when it reaches capacity.

It is widely used in:
  -  Operating Systems (page replacement policies)
  -  Databases (caching frequently accessed queries)
  -  Web Browsers (storing recent pages for fast retrieval)

Working Principle
  -  If a key is accessed, it is moved to the most recently used position.
  -  If a new key is inserted and the cache is full, the least recently used (oldest) item is removed.
  -  Accessing or inserting a key should be done in O(1) time complexity for efficiency.

## How This Implementation is Optimized?

✅ Operations in O(1) Time Complexity
  -  get(key) → O(1) using OrderedDict (dict lookup is O(1), and move operation is O(1)).
  -  put(key, value) → O(1) using OrderedDict (insert/move to end is O(1), and removal of LRU item is O(1)).
✅ Efficient Removal of LRU Items
  -  `popitem(last=False)` removes the first inserted (least recently used) element in O(1).
✅ Maintains Order of Access
  -  `move_to_end(key)` keeps the most recently used items at the end.

## Why Use OrderedDict?

### Advantages of OrderedDict Over Normal Dict
✅ Maintains order of key insertion → When a key is accessed, it is moved to the end. <br/>
✅ Fast access to the least recently used key → The first element is always the least recently used. <br/>
✅ O(1) operations for get, put, and eviction → move_to_end and popitem ensure fast updates. <br/>

In contrast, a normal Python dictionary (dict) does not guarantee order in older versions (<Python 3.7).


#  Doubly Linked List + HashMap Approach (O(1) Solution)

##  Why Use This Approach?
While OrderedDict is simple, an alternative approach is using a Doubly Linked List combined with a HashMap, which also provides O(1) operations.

### Structure
  1.  Doubly Linked List → Stores keys in access order (most recent at the end, least recent at the front).
  2.  HashMap (dict) → Maps keys to Doubly Linked List nodes for O(1) lookup.

##  How This Achieves O(1) Operations?

|  Operation	| Time Complexity |	Why? | <br/>
|  :---:  |  :---:  |  :---:  | <br/>
|  get(key)	|  O(1)	|  HashMap lookup + moving node in DLL  | <br/>
|  :---:  |  :---:  |  :---:  | <br/>
|  put(key, value) |	O(1)	|  HashMap insert + adding/removing DLL node  | <br/>
|  :---:  |  :---:  |  :---:  | <br/>
|  evict LRU	|  O(1)	|  Remove first node from DLL  | <br/>
|  :---:  |  :---:  |  :---:  |


##  Why Doubly Linked List?
  -  Efficient removal: Can remove a node in O(1).
  -  Efficient addition: Can add a node to the end in O(1).
  -  Maintains order of access: Oldest items are at the front.

##  Why HashMap?
  -  Direct lookup in O(1) instead of searching through a list.

#  Comparison of Both Approaches

|  Approach  |	Pros  |	Cons  | <br/>
|  :---:  |  :---:  |  :---:  |  <br/>
|  OrderedDict  |	Simple, built-in, optimized for LRU  |	Uses extra memory for internal ordering  |  <br/>
|  :---:  |  :---:  |  :---:  |  <br/>
|  DLL + HashMap  |	True O(1) performance, custom implementation  |  	More complex to implement  |  <br/>
|  :---:  |  :---:  |  :---:  |  <br/>
