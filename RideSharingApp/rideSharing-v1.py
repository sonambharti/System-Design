"""
# Implement Ride Sharing Application

# How This Works
Users: Riders and Drivers are subclasses of User.
Rider Actions: Request a ride and cancel a ride.
Driver Actions: Accept a ride, complete a ride, and change availability.
Ride Service: Manages ride creation, driver assignments, and ride status updates.
Matching Logic: The system finds the first available driver.
This structure ensures modularity and scalability, aligning with OOP principles.
"""

import uuid
from typing import List, Dict

class User:
    def __init__(self, name: str, user_type: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.user_type = user_type  # 'rider' or 'driver'

class Rider(User):
    def __init__(self, name: str):
        super().__init__(name, 'rider')
        self.current_ride = None

    def request_ride(self, pickup: str, destination: str, ride_service):
        if self.current_ride:
            print(f"{self.name} already has an ongoing ride.")
            return
        self.current_ride = ride_service.create_ride(self, pickup, destination)

    def cancel_ride(self, ride_service):
        if self.current_ride:
            ride_service.cancel_ride(self.current_ride)
            self.current_ride = None
        else:
            print("No active ride to cancel.")

class Driver(User):
    def __init__(self, name: str):
        super().__init__(name, 'driver')
        self.is_available = True
        self.current_ride = None

    def accept_ride(self, ride):
        if self.is_available and ride.status == "Waiting":
            self.is_available = False
            self.current_ride = ride
            ride.assign_driver(self)
            print(f"{self.name} accepted the ride.")
        else:
            print("Ride already taken or driver not available.")

    def complete_ride(self):
        if self.current_ride:
            self.current_ride.complete()
            self.is_available = True
            self.current_ride = None

class Ride:
    def __init__(self, rider: Rider, pickup: str, destination: str):
        self.id = str(uuid.uuid4())
        self.rider = rider
        self.pickup = pickup
        self.destination = destination
        self.driver = None
        self.status = "Waiting"  # Waiting, In Progress, Completed, Cancelled

    def assign_driver(self, driver: Driver):
        self.driver = driver
        self.status = "In Progress"

    def complete(self):
        self.status = "Completed"
        print(f"Ride {self.id} completed successfully!")

class RideService:
    def __init__(self):
        self.rides: List[Ride] = []
        self.drivers: List[Driver] = []

    def register_driver(self, driver: Driver):
        self.drivers.append(driver)

    def create_ride(self, rider: Rider, pickup: str, destination: str) -> Ride:
        ride = Ride(rider, pickup, destination)
        self.rides.append(ride)
        print(f"Ride requested by {rider.name} from {pickup} to {destination}.")
        return ride

    def cancel_ride(self, ride: Ride):
        if ride.status == "Waiting":
            ride.status = "Cancelled"
            print(f"Ride {ride.id} has been cancelled.")
        else:
            print("Cannot cancel an ongoing or completed ride.")

    def find_available_driver(self):
        for driver in self.drivers:
            if driver.is_available:
                return driver
        return None

# Example Usage
def main():
    service = RideService()

    rider1 = Rider("Alice")
    driver1 = Driver("Bob")
    driver2 = Driver("Charlie")
    
    service.register_driver(driver1)
    service.register_driver(driver2)

    rider1.request_ride("Point A", "Point B", service)
    available_driver = service.find_available_driver()
    if available_driver:
        available_driver.accept_ride(rider1.current_ride)
        available_driver.complete_ride()
    else:
        print("No available drivers.")

if __name__ == "__main__":
    main()
