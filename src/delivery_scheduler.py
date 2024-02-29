import datetime

class DeliveryScheduler:
    def __init__(self, addressCSV, distanceCSV, packageHash):
        self.addressCSV = addressCSV
        self.distanceCSV = distanceCSV
        self.packageHash = packageHash
        
    # Sort packages by deadline, prioritizing those with specific deadlines over EOD deadlines
    def sortPackagesByDeadline(self, packageIDs):
        sortedPackages = sorted(
            [self.packageHash.search(packageID) for packageID in packageIDs],
            # Sort by whether the deadline is not EOD, then by the deadline itself
            key=lambda p: (p.deadline != 'EOD', p.deadline),
            reverse=True # True to prioritize earlier deadlines
        )
        return [p.ID for p in sortedPackages]

    # Find the index of an address in the addressCSV data
    def findLocationIndex(self, address):
        for i, addressEntry in enumerate(self.addressCSV):
            if address == addressEntry[2]:
                return i
        return None

    # Convert a package address to its corresponding index in addressCSV
    def convertAddressToIndex(self, packageAddress):
        for i, addressEntry in enumerate(self.addressCSV):
            if packageAddress == addressEntry[2]:
                return i
        return None

    # Retrieve the distance between two locations using distanceCSV data
    def getDistance(self, currentLocationIndex, destinationIndex):
        if self.distanceCSV[currentLocationIndex][destinationIndex] != '':
            return float(self.distanceCSV[currentLocationIndex][destinationIndex])
        else:
            return float(self.distanceCSV[destinationIndex][currentLocationIndex])

    # Find the nearest location from a given location among remaining package destinations
    def findNearestLocation(self, currentLocation, packageDestinations):
        nearestLocation = min(packageDestinations, key=lambda loc: self.getDistance(currentLocation, loc))
        minDistance = self.getDistance(currentLocation, nearestLocation)
        return nearestLocation, minDistance

    # Select the next package to deliver based on expected delivery time and deadline
    def selectNextPackage(self, truck, sortedPackageIDs, departureDateTime, totalMiles):
        expectedDeliveryTime = departureDateTime + datetime.timedelta(hours=totalMiles / truck.speed)
        for i, packageID in enumerate(sortedPackageIDs):
            package = self.packageHash.search(packageID)
            deadlineDatetime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(package.deadline, '%I:%M %p').time()) if package.deadline != 'EOD' else datetime.datetime.max
            if expectedDeliveryTime <= deadlineDatetime:
                return i
        return None

    # Calculate the delivery time based on distance and speed
    def calculateDeliveryTime(self, distance, speed):
        return datetime.timedelta(hours=distance / speed)

    # Update the delivery time and status of a delivered package
    def updatePackageDeliveryTime(self, package, truck, totalMiles):
        package.deliveryTime = truck.departTime + datetime.timedelta(hours=totalMiles / truck.speed)
        package.status = "Delivered"
        
    # Return the truck to the hub and update total miles
    def returnToHub(self, truck, currentLocationIndex, totalMiles):
        truckCurrentLocationIndex = self.findLocationIndex(truck.currentLocation)
        if truckCurrentLocationIndex is not None:
            totalMiles += self.getDistance(currentLocationIndex, truckCurrentLocationIndex)
        truck.miles = totalMiles
        return totalMiles

    # Main delivery algorithm (Greedy-Nearest Neighbor)
    def deliveryAlgorithm(self, truck):
        departureDateTime = datetime.datetime.combine(datetime.date.today(), (datetime.datetime.min + truck.departTime).time())
        sortedPackageIDs = self.sortPackagesByDeadline(truck.packages)

        # Special handling for package 9 (always deliver last)
        if 9 in sortedPackageIDs:
            sortedPackageIDs.remove(9)
            sortedPackageIDs.append(9)
        truck.packages = sortedPackageIDs

        # Set departure time for packages
        for packageID in truck.packages:
            package = self.packageHash.search(packageID)
            if package:
                package.departureTime = truck.departTime

        totalMiles = 0
        currentLocationIndex = self.findLocationIndex(truck.currentLocation)
        if currentLocationIndex is None:
            print(f"Current location not found in addressCSV: {truck.currentLocation}")
            return

        packageDestinations = [self.convertAddressToIndex(self.packageHash.search(packageID).street) for packageID in sortedPackageIDs]

        while packageDestinations:
            nearest, distanceToNearest = self.findNearestLocation(currentLocationIndex, packageDestinations)
            totalMiles += distanceToNearest
            truck.time += self.calculateDeliveryTime(distanceToNearest, truck.speed)

            nextPackageIndex = self.selectNextPackage(truck, truck.packages, departureDateTime, totalMiles)
            if nextPackageIndex is not None:
                deliveredPackageID = truck.packages.pop(nextPackageIndex)
                deliveredPackage = self.packageHash.search(deliveredPackageID)
                if deliveredPackage:
                    self.updatePackageDeliveryTime(deliveredPackage, truck, totalMiles)
                currentLocationIndex = nearest
                packageDestinations.remove(nearest)
            else:
                print("Unable to meet the deadline for remaining packages.")
                break

        totalMiles = self.returnToHub(truck, currentLocationIndex, totalMiles)
