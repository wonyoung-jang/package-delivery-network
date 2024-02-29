import csv
from package import Package

# Load Package CSV Function
def loadPackageData(filename, hash_table):
    try:
        with open(filename) as packages:
            packageData = csv.reader(packages, delimiter=',')
            next (packageData) # Skip header row in package.csv
            for package in packageData:
                id = int(package[0])
                street = package[1]
                city = package[2]
                state = package[3]
                zip = package[4]
                deadline = package[5]
                weight = package[6]
                notes = package[7]
                status = "At the Hub" # Initial status
                departureTime = None
                deliveryTime = None
                
                # Insert package data into hash_table
                p = Package(id, street, city, state, zip, deadline, weight, notes, status, departureTime, deliveryTime)
                hash_table.insert(id, p)
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return hash_table

def loadAddressAndDistanceData(filename):
    with open(filename) as name:
            name = csv.reader(name)
            return list(name)
