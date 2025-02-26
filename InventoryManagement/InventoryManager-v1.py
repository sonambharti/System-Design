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


import time
from threading import Timer

class InventoryManager:
    def __init__(self):
        self.products = {}
        self.orders = {}
        self.blocked_inventory = {}

    def createProduct(self, productId, name, count):
        self.products[productId] = {"name": name, "count": count}
        print(f'Product created: {productId} -> ({name}, {count})')

    def getInventory(self, productId):
        if productId in self.products:
            return self.products[productId]["count"]
        return "Product not found"

    def createOrder(self, productIds, quantityOrdered, orderId):
        if orderId in self.orders:
            return "Order already exists"

        self.orders[orderId] = {"productIds": productIds, "quantityOrdered": quantityOrdered, "status": "blocked"}
        for productId, quantity in zip(productIds, quantityOrdered):
            if self.products[productId]["count"] < quantity:
                return "Not enough inventory"
            self.products[productId]["count"] -= quantity
            if productId not in self.blocked_inventory:
                self.blocked_inventory[productId] = 0
            self.blocked_inventory[productId] += quantity
            print(f'{quantity} quantity of product {productId} blocked for order {orderId}')

        # Bonus feature: automatically cancel order if not confirmed within 5 minutes
        Timer(300, self._autoCancelOrder, [orderId]).start()

    def confirmOrder(self, orderId):
        if orderId in self.orders and self.orders[orderId]["status"] == "blocked":
            self.orders[orderId]["status"] = "confirmed"
            for productId, quantity in zip(self.orders[orderId]["productIds"], self.orders[orderId]["quantityOrdered"]):
                self.blocked_inventory[productId] -= quantity
            print(f'Order {orderId} confirmed')
        else:
            return "Order not found or already confirmed/canceled"

    def cancelOrder(self, orderId):
        if orderId in self.orders and self.orders[orderId]["status"] == "blocked":
            self.orders[orderId]["status"] = "canceled"
            for productId, quantity in zip(self.orders[orderId]["productIds"], self.orders[orderId]["quantityOrdered"]):
                self.products[productId]["count"] += quantity
                self.blocked_inventory[productId] -= quantity
            print(f'Order {orderId} canceled')
        else:
            return "Order not found or already confirmed/canceled"

    def _autoCancelOrder(self, orderId):
        if orderId in self.orders and self.orders[orderId]["status"] == "blocked":
            self.cancelOrder(orderId)

# Driver code for demo purposes
if __name__ == "__main__":
    inv_manager = InventoryManager()

    # Creating products
    inv_manager.createProduct("ProductId1", "Laptop", 2)
    inv_manager.createProduct("ProductId2", "Mobile", 5)
    inv_manager.createProduct("ProductId3", "Earphone", 4)

    # Getting inventory
    print(f'Inventory of ProductId1: {inv_manager.getInventory("ProductId1")}')
    print(f'Inventory of ProductId2: {inv_manager.getInventory("ProductId2")}')
    print(f'Inventory of ProductId3: {inv_manager.getInventory("ProductId3")}')

    # Creating orders
    inv_manager.createOrder(["ProductId1", "ProductId3"], [1, 2], "OrderId1")

    # Confirming orders
    inv_manager.confirmOrder("OrderId1")

    # Canceling orders
    inv_manager.createOrder(["ProductId1", "ProductId3"], [1, 2], "OrderId2")
    inv_manager.cancelOrder("OrderId2")
