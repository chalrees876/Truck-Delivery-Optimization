#C950 TASK 2

#By Chris McKenzie
#Student i = 012340722



import csv
import re

from package import Package
from hash import HashTable
from truck import Truck


def main():

    #Call function to add all packages in csv into hash table.
    hashtable = hash_packages("Resources/packages.csv")

    distance_table = get_distances("Resources/distances.csv")

    truck1 = Truck(1)

    for i in range(hashtable.size):
        for package in hashtable.data[i]:
            if package not in truck1.packages_loaded:
                truck1.add_package(package)

    truck1_packages = truck1.packages_loaded
    truck1_table = make_truck_table(truck1_packages, distance_table)

    first_stop_distance = float(distance_from_hub(truck1_table, hashtable.get(4).address))

    truck1.deliver_package(hashtable.get(4), first_stop_distance)
    hashtable.get(4).print_info()


    for i in range(40):
        package_delivered = False
        closest_neighbor_address = closest_neighbor(truck1.current_location, truck1_table)

        print(closest_neighbor_address)

        for package in truck1.packages_loaded:
            if package.address.strip().lower() in closest_neighbor_address.strip().lower():
                print("Package found", package.package_id)
                next_distance = find_address_distances(truck1.current_location, package.address, truck1_table)
                truck1.deliver_package(package, next_distance)
                package.print_info()
                package_delivered = True
        if package_delivered is False:
            find_address_distances(truck1.current_location, closest_neighbor_address, truck1_table)

def make_truck_table(packages, distance_table):
    keep_columns = {0}
    for column_index, column in enumerate(distance_table[7]):
        for package in packages:
            if package.address in column:
                keep_columns.add(column_index)

    keep_rows = {7}
    for row_index, row in enumerate(distance_table):
        for package in packages:
            if package.address in row[0]:
                keep_rows.add(row_index)


    truck_table = []
    for row_index in keep_rows:
        row = distance_table[row_index]
        truck_table_row = [row[column_index] for column_index in keep_columns]
        truck_table.append(truck_table_row)

    return truck_table



def find_address_distances(address1, address2, distance_table):
    address1_row = -1
    address2_col = -1

    # Find row index for address1
    for row_index, row in enumerate(distance_table[1:], start=1):  # skip header row
        if address1.strip().lower() in row[0].strip().lower():
            address1_row = row_index
            break

    # Find column index for address2
    for col_index, col in enumerate(distance_table[0][2:], start=2):  # skip first two columns
        if address2.strip().lower() in col.strip().lower():
            address2_col = col_index
            break

    if address1_row == -1 or address2_col == -1:
        print(f"Could not find row/column for addresses: '{address1}' or '{address2}'")
        return "Error"

    # Try normal direction
    try:
        val = distance_table[address1_row][address2_col]
        if val.strip() != "":
            distance = float(val.strip())
            distance_table[address1_row][address2_col] = "100"
            return distance
    except:
        pass

    # Try symmetric direction
    try:
        val = distance_table[address2_col - 1 + 1][address1_row + 1]
        if val.strip() != "":
            distance = float(val.strip())
            distance_table[address2_col - 1 + 1][address1_row + 1] = "100"
            return distance
    except:
        pass

    return "Error"



def distance_from_hub(distance_table, address):
    for row in distance_table:
        if address in row[0]:
            distance = row[3]
            return float(distance)

def closest_neighbor(address, distance_table):
    row_index = None
    min_distance_row = 100
    min_distance_column = 100
    #determine what row address is in
    for i, row in enumerate(distance_table):
        if address in row[0]:
            row_index = i
            break
    if row_index is None:
        print("Address not found", address)
        print("looking in ")
        return None

    #determine what column address is in
    column_index = None
    for i, item in enumerate(distance_table[0]):
        if address.strip() in item.strip():
            column_index = i
            break
    if column_index is None:
        print("column index not found for this address", address)
        return None

    min_distance_row_index = 0
    min_distance_column_index = 0
    for index, item in enumerate(distance_table[row_index]):
        if len(item) == 3 or len(item) == 4:
            if min_distance_column > float(item) > 0:
                min_distance_column = float(item)
                min_distance_column_index = index

    for index, item in enumerate(distance_table):
        if len(item[column_index]) == 3 or len(item[column_index]) == 4:
            if min_distance_row > float(item[column_index]) > 0:
                min_distance_row = float(item[column_index])
                min_distance_row_index = index

    if min_distance_row < min_distance_column:
        closest_neighbor_address = distance_table[min_distance_row_index][0]
    else:
        closest_neighbor_address = distance_table[0][min_distance_column_index]

    return closest_neighbor_address


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

            #Create packages for each row in the csv file.
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], int(row[6]))

            #Take care of edge cases
            if row[7] == "Can only be on truck 2":
                package.truck = 2

            elif row[7] == "Delayed on flight---will not arrive to the depot until 9:05 am":
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


if __name__ == "__main__":
    main()





