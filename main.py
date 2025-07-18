#C950 TASK 2

#By Chris McKenzie
#Student i = 012340722



import csv
import re
from symbol import continue_stmt

from package import Package
from hash import HashTable
from truck import Truck


def main():

    #Call function to add all packages in csv into hash table.
    hashtable = hash_packages("Resources/packages.csv")

    #Create a distance table
    distance_table = get_distances("Resources/distances.csv")

    truck1 = Truck(1)
    truck2 = Truck(2)

    #loop until all packages have been delivered
    while any(
            package.status != "Delivered"
            for bucket in hashtable.data
            for package in bucket
    ):

        #load packages onto truck 1
        load_packages(truck1, hashtable)


        # load and deliver package 37
        # I do this because initially it gets placed onto truck 1
        # and in my current algorithm it delivers package 37 last
        # this makes package 37 miss its deadline
        # i only want to do this inside the loop if package 37 is not delivered
        package37 = hashtable.get(37)
        if package37.status != "Delivered":
            package37_distance_from_hub = distance_from_hub(distance_table, package37.address)
            truck2.add_package(package37)
            truck2.deliver_package(package37, package37_distance_from_hub)
            truck2.drive_to_hub(package37_distance_from_hub)

            # I want to set truck 2 current time to 9:06 am so it can pick up all the delayed packages
            if convert_string_time_to_int(truck2.current_time) < convert_string_time_to_int("9:06 AM"):
                truck2.current_time = "9:06 AM"
        load_packages(truck2, hashtable)

        # algorithm finds the package with the earliest deadline and delivers that package first
        deliver_first_package(truck1, distance_table, hashtable)
        deliver_first_package(truck2, distance_table, hashtable)

        #this delivers the rest of the packages on the truck in order of their nearest neighbor
        deliver_packages(truck1, distance_table, hashtable)
        deliver_packages(truck2, distance_table, hashtable)

    print("Enter package ID you would like to check the status of. Or type \"all\"")
    package_id_input = input(">>> ")
    print("What time is it? (HH:MM AM|PM)")
    time = input(">>> ")
    while True:
        if package_id_input == "all":
            for i in range(hashtable.size):
                for package in hashtable.data[i]:
                    get_package_info_at_time(package, time)
            break
        elif package_id_input.isdigit():
            try:
                package_id = int(package_id_input)
            except:
                break
            get_package_info_at_time(hashtable.get(package_id), time)
            break
        else:
            print("Unknown Command")
            break
    print("Would you like truck info? (y/n)")
    while True:
        answer = input(">>> ")
        if answer.lower() == "y":
            truck1_miles = get_miles_driven_by_time(truck1, time)
            truck2_miles = get_miles_driven_by_time(truck2, time)
            print("at", time, "truck 1 has driven", truck1_miles, "miles")
            print("at", time, "truck 2 has driven", truck2_miles, "miles")
            break


def get_miles_driven_by_time(truck, time_check):
    miles = 0.0
    time_check_int = convert_string_time_to_int(time_check)
    for delivery_time, distance in truck.delivery_log:
        delivery_time_int = convert_string_time_to_int(delivery_time)
        if delivery_time_int <= time_check_int:
            miles += distance
    return round(miles)


def get_package_info_at_time(package, time):
    current_time = convert_string_time_to_int(time)
    package_delivered_time = convert_string_time_to_int(package.time_delivered)
    package_loaded_time = convert_string_time_to_int(package.loaded_time)
    if current_time >= package_delivered_time:
        print("Package", package.package_id, "was delivered at", package.time_delivered)
        return
    if package_delivered_time > current_time >= package_loaded_time:
        print("Package", package.package_id, "was loaded on to truck", package.truck, "at", package.loaded_time, "and is en route")
        return
    else:
        print("Package", package.package_id, "is at the hub")
        return


def deliver_first_package(truck, distance_table, hashtable):
    earliest_deadline = convert_string_time_to_int("5:01 PM")
    earliest_deadline_idx = 0
    for idx, package in enumerate(truck.packages_loaded):
        if convert_string_time_to_int(package.deadline) < earliest_deadline:
            earliest_deadline = convert_string_time_to_int(package.deadline)
            earliest_deadline_idx = idx
    package = truck.packages_loaded[earliest_deadline_idx]
    package_distance_from_hub = distance_from_hub(distance_table, package.address)

    truck.deliver_package(package, package_distance_from_hub)

def deliver_packages(truck, distance_table, hashtable):
    for i in range(len(truck.packages_loaded)):
        neighbors = get_neighbors_sorted_by_distance(truck.current_location, distance_table)
        found_package = False

        for neighbor in neighbors:
            for package in truck.packages_loaded:
                if package.address in neighbor[0]:
                    found_package = True
                    truck.deliver_package(package, neighbor[1])

                    # Handle delivered_with logic
                    if package.delivered_with:
                        for package_id in package.delivered_with:
                            related_package = hashtable.get(package_id)
                            if (
                                    related_package in truck.packages_loaded
                                    and related_package.truck == truck.number
                            ):
                                truck.deliver_package(related_package, distance_between_addresses(package.address, related_package.address, distance_table))
                    break  # prevent delivering multiple packages to same neighbor
            if found_package:
                break
    truck.drive_to_hub(distance_from_hub(distance_table, truck.current_location))



def load_packages(truck, hashtable):
    for i in range(hashtable.size):
        #adding packages by zip code
        current_zip = ""
        for package in hashtable.data[i]:
            current_zip = package.zipcode
            #loop through packages again to put in same zip codes
            for j in range(hashtable.size):
                for nested_package in hashtable.data[j]:
                    if (
                    len(truck.packages_loaded) < 16
                    and nested_package.zipcode == current_zip
                    and nested_package.status == "In hub"
                    and convert_string_time_to_int(nested_package.delayed_time) <= convert_string_time_to_int(truck.current_time)
                    and (nested_package.truck is None or nested_package.truck == truck.number)
                    ):
                        truck.add_package(nested_package)
                        if nested_package.delivered_with:
                            for package_id in nested_package.delivered_with:
                                dependent_package = hashtable.get(package_id)
                                if (len(truck.packages_loaded) < 16
                                        and dependent_package.status == "In hub"
                                        and convert_string_time_to_int(dependent_package.delayed_time) <= convert_string_time_to_int(truck.current_time)
                                ):
                                    truck.add_package(hashtable.get(package_id))


def distance_from_hub(distance_table, address):
    if address == "HUB":
        return 0
    for row in distance_table:
        if address in row[0]:
            distance = row[2]
            return float(distance)

def distance_between_addresses(address1, address2, distance_table):

    if address1 == address2:
        return 0
    address1_row = -1
    address1_col = -1
    address2_row = -1
    address2_col = -1
    for row_idx, row in enumerate(distance_table):
        if address1 in row[0]:
            address1_row = row_idx
        if address2 in row[0]:
            address2_row = row_idx
    for col_idx, col in enumerate(distance_table[0]):
        if address2 in col:
            address2_col = col_idx
        if address1 in col:
            addres1_col = col_idx

    try:
        dist = float(distance_table[address1_row][address2_col])
        if dist >= 0:
            return dist
    except (ValueError, TypeError):
        pass  # Not a float, or invalid type

    # Try the second one
    try:
        dist = float(distance_table[address2_row][address1_col])
        if dist >= 0:
            return dist
    except (ValueError, TypeError):
        pass




def get_neighbors_sorted_by_distance(address, distance_table):
    neighbors = []

    # Get the row and column indices for the address
    row_idx = None
    col_idx = None

    #check row headers for address
    for i, row in enumerate(distance_table):
        if address.strip().lower() in row[0].lower():
            row_idx = i
            break
    if row_idx is None:
        print("row not found")
    #check column headers for address
    for i, item in enumerate(distance_table[0]):
        if address.strip().lower() in item.lower():
            col_idx = i
            break
    if col_idx is None:
        print("col not found")

    if row_idx is None or col_idx is None:
        return []

    #add distanced from all rows and columns into neighbors list
    for idx, row in enumerate(distance_table):
        try:
            dist = float(row[col_idx])
            if dist >= 0:
                neighbors.append((distance_table[idx][0], dist))
        except:
            continue
    for idx, col in enumerate(distance_table[row_idx]):
        try:
            dist = float(col)
            if dist >= 0:
                neighbors.append((distance_table[idx][0], dist))
        except:
            continue

    # Sort by distance
    neighbors.sort(key=lambda x: x[1])
    return neighbors



def get_distances(distance_file):
    distance_table = []
    with open(distance_file, mode='r') as file:
        for row in csv.reader(file):
            # Strip leading/trailing spaces and remove newlines
            cleaned_row = [cell.strip().replace('\n', ' ') for cell in row]
            distance_table.append(cleaned_row)
    return distance_table



def hash_packages(packages_file):

    #Create empty hashtable
    hashtable = HashTable()

    with open(packages_file, mode='r') as file:
        for row in csv.reader(file):

            if "EOD" in row[5]:
                row[5] = "5:00 PM"
            #Create packages for each row in the csv file.
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], int(row[6]))

            #Take care of edge cases
            if row[7] == "Can only be on truck 2":
                package.truck = 2

            elif "Delayed" in row[7]:
                package.delayed_time = "9:05 AM"

            elif row[7] == "Wrong address listed":
                package.incorrect_address = True
                package.delayed_time = "10:20 AM"

            elif "Must be delivered with" in row[7]:
                numbers = re.findall(r'\d+', row[7])
                for num in numbers:
                    package.delivered_with.append(int(num))

            hashtable.insert(package)
        return hashtable


def convert_string_time_to_int(time):
    if time is None:
        return 0
    match = re.match(r"^(\d{1,2}):(\d{2}) (AM|PM)$", time.strip())
    if not match:
        raise ValueError(f"Invalid time format: {time}")

    hour = int(match.group(1))
    minute = int(match.group(2))
    period = match.group(3)

    # Convert to minutes since midnight
    total_minutes = hour % 12 * 60 + minute
    if period == "PM":
        total_minutes += 12 * 60

    return total_minutes

if __name__ == "__main__":
    main()





