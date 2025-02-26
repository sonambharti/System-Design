"""
# Problem statement:


# Develop a program to manage the inventory for an e-commerce company. In this e-commerce website, Admin will create the products which will be visible to the customers, The customer can place an order via online payment. Before initiating online payment, we will block the inventory, until it completes the payment.


# Methods to implement:
# 1. create product with given productid, name and inventory count
# createProduct(String productId, String name, Integer count)
 
# 2. return the available quantity for given product
# getinventory(String productid)

# 3. Will be called when the user initiates payment for an order.This will block ordered quantity for the given product and for the given order reference 
# createOrder(List<String> productIds, List<Integer> quantityOrdered, String orderId)
 
# 4. Will be called when the user completes payment for his order. Reduce the ordered quantity permanently for the product corresponding to given orderId.
# confirmOrder(String orderId)


# 5. Will be called when the user cancels payment for his order. The blocked quantity should be released back.
# cancelOrder(String orderId)

# Mandatory use case: 
# All 5 functions should be working and implemented
# Bonus Use case:
# If confirmOrder() is not called within 5min from createOrder(), cancel the order.



# Note: Please focus on the Bonus Feature only after ensuring the required features are complete and demoable. 
# Note: Bonus will be considered only if the required functionality is working.
# Note:ith index of quantityOrdered will be be the quantity of the ith productIds
# Note:An order can have multiple products



# Things to take care of:
# You are free to use the IDE of your choice.
# You can use any library in you code
# You are free to use the language of your choice.
# No External Database(Mysql) is required, you can use in-memory Database, like List, Map etc…
# Do not use any database or NoSQL store, use in-memory store for now.
# Do not create any UI for the application.
# Write a driver class for demo purposes. Which will execute all the commands at one place in the code and test cases.
# The code should be executable (no compiler errors) 
# Demonstration of all the functionalities is important.
# Complete coding within the duration of 60 minutes.
# Use intuitive variable names, function names, class names etc.
# All work should be your own. If found otherwise, you may be disqualified.



# Good to have:
# Modular and clean code.
# Proper naming convention
# Bonus case implementation


    


# HAPPY TEST CASES


# createProduct("ProductId1", "Laptop", 2)


# "ProductId1" -> (Laptop, 2)


# createProduct("2", "Mobile", 5)


# "ProductId2" -> (Mobile, 5)


# createProduct("ProductId3", "Earphone", 4)


# "ProductId3" -> (Earphone, 4)


# getInventory("ProductId1")


# 2


# getInventory("ProductId2")


# 5


# getInventory("ProductId3")


# 4


# createOrder(["ProductId1", "ProductId3"], [1, 2], "OrderId1")


# "ProductId1" -> 1 quantity blocked
# "ProductId3" -> 2 quantity blocked


# confirmOrder("OrderId1")


# "OrderId1" -> (Laptop, 1)


# "OrderId2" -> (ProductId3, 2)
product_details = {}
# product_details[1] = {'name': 'Sonam', 'comp':'Paras'}
# print(product_details[1]['name'])
create_order = {}
# Order_key = {}
"""

import threading
import time

class InventoryManager:
    def __init__(self):
        self.products = {}  # Stores product details {productId: {'name': name, 'count': count}}
        self.orders = {}  # Stores order details {orderId: {'products': {productId: quantity}, 'timestamp': timestamp}}
        self.lock = threading.Lock()  # Lock to ensure thread safety

    def createProduct(self, productId, name, count):
        """Adds a new product to the inventory."""
        with self.lock:
            self.products[productId] = {'name': name, 'count': count}
        print(f"Product created: {productId} -> ({name}, {count})")

    def getInventory(self, productId):
        """Returns the available inventory count for a given product."""
        with self.lock:
            return self.products.get(productId, {}).get('count', 0)

    def createOrder(self, productIds, quantityOrdered, orderId):
        """Blocks inventory for an order and starts a timer to auto-cancel after 5 minutes."""
        with self.lock:
            if orderId in self.orders:
                print("Order ID already exists!")
                return
            
            for productId, quantity in zip(productIds, quantityOrdered):
                if productId not in self.products or self.products[productId]['count'] < quantity:
                    print(f"Insufficient inventory for product {productId}")
                    return
            
            # Block inventory
            self.orders[orderId] = {'products': {}, 'timestamp': time.time()}
            for productId, quantity in zip(productIds, quantityOrdered):
                self.products[productId]['count'] -= quantity
                self.orders[orderId]['products'][productId] = quantity
                print(f"Product {productId} -> {quantity} quantity blocked")
            
            # Start a timer for auto-cancel if not confirmed in 5 minutes
            timer = threading.Timer(300, self.autoCancelOrder, [orderId])
            timer.start()
    
    def confirmOrder(self, orderId):
        """Confirms an order and permanently deducts blocked inventory."""
        with self.lock:
            if orderId not in self.orders:
                print("Order ID not found!")
                return
            
            print(f"Order {orderId} confirmed:")
            for productId, quantity in self.orders[orderId]['products'].items():
                print(f"{productId} -> {quantity} quantity deducted permanently")
            
            del self.orders[orderId]  # Remove order from tracking
    
    def cancelOrder(self, orderId):
        """Cancels an order and restores the blocked inventory."""
        with self.lock:
            if orderId not in self.orders:
                print("Order ID not found!")
                return
            
            for productId, quantity in self.orders[orderId]['products'].items():
                self.products[productId]['count'] += quantity
                print(f"Product {productId} -> {quantity} quantity restored")
            
            del self.orders[orderId]  # Remove order from tracking
            print(f"Order {orderId} cancelled.")
    
    def autoCancelOrder(self, orderId):
        """Automatically cancels an order if it is not confirmed within 5 minutes."""
        with self.lock:
            if orderId in self.orders:
                print(f"Auto-cancelling order {orderId} due to timeout.")
                self.cancelOrder(orderId)

# Example execution
def main():
    manager = InventoryManager()
    
    # Creating products
    manager.createProduct("ProductId1", "Laptop", 2)
    manager.createProduct("ProductId2", "Mobile", 5)
    manager.createProduct("ProductId3", "Earphone", 4)
    
    # Checking inventory
    print("Inventory ProductId1:", manager.getInventory("ProductId1"))
    print("Inventory ProductId2:", manager.getInventory("ProductId2"))
    print("Inventory ProductId3:", manager.getInventory("ProductId3"))
    
    # Placing an order
    manager.createOrder(["ProductId1", "ProductId3"], [1, 2], "OrderId1")
    
    # Confirming the order
    manager.confirmOrder("OrderId1")
    
    # Cancelling an order (if needed)
    # manager.cancelOrder("OrderId1")  # Uncomment to test manual cancel
    
if __name__ == "__main__":
    main()
