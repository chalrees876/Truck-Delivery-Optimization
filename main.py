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

    truck1_table = make_truck_table(truck1.packages_loaded, distance_table)

    first_stop_distance = float(distance_from_hub(truck1_table, hashtable.get(4).address))

    truck1.deliver_package(hashtable.get(4), first_stop_distance)
    hashtable.get(4).print_info()

    get_neighbors_sorted_by_distance(truck1.current_location, truck1_table)

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
    for row_index, row in enumerate(distance_table):  # skip header row
        if address1.strip().lower() in row[0].strip().lower():
            print("found address1")
            address1_row = row_index
            break

    # Find column index for address2
    for col_index, col in enumerate(distance_table[7]):  # skip first two columns
        if address2.strip().lower() in col.strip().lower():
            print("found address2")
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
            return distance
    except:
        pass

    # Try symmetric direction
    try:
        val = distance_table[address2_col - 1 + 1][address1_row + 1]
        if val.strip() != "":
            distance = float(val.strip())
            return distance
    except:
        pass

    return "Error"



def distance_from_hub(distance_table, address):
    for row in distance_table:
        if address in row[0]:
            distance = row[3]
            return float(distance)

def get_neighbors_sorted_by_distance(address, distance_table):
    neighbors = []

    # Get the row and column indices for the address
    row_idx = None
    col_idx = None

    for i, row in enumerate(distance_table):
        if address.strip().lower() in row[0].lower():
            row_idx = i
            break
    for i, item in enumerate(distance_table[0]):
        if address.strip().lower() in item.lower():
            col_idx = i
            break

    if row_idx is None or col_idx is None:
        return []

    # Collect distances to all other addresses
    for idx, row in enumerate(distance_table):
        try:
            dist = float(row[col_idx])
            if dist > 0:
                neighbors.append((distance_table[idx][0], dist))
        except:
            continue
    for idx, col in enumerate(distance_table[row_idx]):
        try:
            dist = float(col)
            if dist > 0:
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





