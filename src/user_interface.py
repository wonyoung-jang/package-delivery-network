import datetime

class UserInterface:
    def __init__(self, packageHash, truck1, truck2, truck3):
        # Print project title
        print("University Parcel Service")

        # Print total mileage of all trucks
        print ("Total Mileage of All Trucks:", (truck1.miles + truck2.miles + truck3.miles))

        # Format string for output
        formatString = "{:<10} {:<40} {:<20} {:<10} {:<10} {:<15} {:<12} {:<15} {:<15} {:<15}"

        # Interactive User Interface
        while True:
            try:
                # Prompt user for a lookup time
                userTime = input("Enter a time to see status of package(s). Format: HH:MM. ")
                (h, m) = userTime.split(":")
                timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
            
                # Prompt user for a package ID | Allows seeing all packages
                try:
                    singleEntry = [int(input("Enter Package ID to see it's status or nothing to see all."))]
                except ValueError:
                    singleEntry =  range(1, 41)
                
                # Print package data header
                print(formatString.format("ID", "Address", "City", "State", "Zip", "Deadline", "Status", "Departure Time", "Delivery Time", "Truck"))

                # Print package data
                for packageID in singleEntry:
                    package = packageHash.search(packageID)
                    package.statusUpdate(timeChange)
                    
                    # Format each line
                    print(formatString.format(
                        package.ID,
                        package.street,
                        package.city,
                        package.state,
                        package.zip,
                        package.deadline,
                        package.status,
                        str(package.departureTime or ""),
                        str(package.deliveryTime or ""),
                        package.truck
                    ))
                    
            except Exception as e:
                print(f"An error occurred: {e} | Please try with the proper format.")