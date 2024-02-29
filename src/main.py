import csv
import datetime
from truck import Truck
from package import Package
from hash_table import HashTable
from delivery_scheduler import DeliveryScheduler
from user_interface import UserInterface
from data_loader import loadPackageData, loadAddressAndDistanceData

if __name__ == "__main__":
    packageHash = HashTable() 
    packageHash = loadPackageData('package.csv', packageHash)
    addressCSV = loadAddressAndDistanceData('address.csv')
    distanceCSV = loadAddressAndDistanceData('distance.csv')
    scheduler = DeliveryScheduler(addressCSV, distanceCSV, packageHash)
    
    # Manually load trucks based off requirements, and assign other values
    truck1 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,2,4,13,14,15,16,19,20,29,30,31,34,37,40])
    truck2 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=12),[3,5,7,8,9,10,11,12,17,18,36,38])
    truck3 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,21,22,23,24,25,26,27,28,32,33,35,39])

    # Manually assign trucks to packages
    packageHash.setTrucksToPackages([truck1, truck2, truck3], [1, 3, 3])
        
    # Calls trucks to leave to deliver packages
    scheduler.deliveryAlgorithm(truck1)
    scheduler.deliveryAlgorithm(truck3)

    # Checks that truck2 will not leave unless truck1 or truck3 have returned
    truck2.departTime = min(truck1.time, truck3.time)
    scheduler.deliveryAlgorithm(truck2)
    
    interface = UserInterface(packageHash, truck1, truck2, truck3)