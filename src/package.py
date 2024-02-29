from datetime import datetime, timedelta

class Package:
    # Stores data about Package object
    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status, departureTime=None, deliveryTime=None, truck=0):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = departureTime
        self.deliveryTime = deliveryTime
        self.truck = truck

    # Update status of package depending entered time
    def statusUpdate(self, timeChange):
        if self.deliveryTime is None or self.departureTime is None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"
        elif self.departureTime <= timeChange < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"

        # Handling package #9
        if self.ID == 9:
            if timeChange > timedelta(hours=10, minutes=20):
                self.street = "410 S State St"  # Update street for package #9 after 10:20
                self.zip = "84111"              # Update ZIP code for package #9 after 10:20
            else:
                self.street = "300 State St"    # Revert street for package #9 to original
                self.zip = "84103"              # Revert ZIP code for package #9 to original
