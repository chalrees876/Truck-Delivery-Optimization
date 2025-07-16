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

    truck1 = Truck()

    for package in hashtable.data[0]:
        truck1.add_package(package)

    truck1_packages = truck1.packages_loaded
    truck1_table = distance_table


    #creates a distance table specific to packages on truck
    truck1_table = make_truck_table(truck1_packages, distance_table)

    first_stop = truck1_packages[0].address

    print(truck1.calculate_time(37, "8:11 AM"))







def make_truck_table(packages, distance_table):
    keep_columns = [0]
    for column_index, column in enumerate(distance_table[7]):
        for package in packages:
            if package.address in column:
                keep_columns.append(column_index)

    keep_rows = [7]
    for row_index, row in enumerate(distance_table):
        for package in packages:
            if package.address in row[0]:
                keep_rows.append(row_index)


    truck_table = []
    for row_index in keep_rows:
        row = distance_table[row_index]
        truck_table_row = [row[column_index] for column_index in keep_columns]
        truck_table.append(truck_table_row)

    return truck_table



def find_address_distances(address1, address2, distance_table):
    address1_row = -1
    address2_col = -1
    for row_index, row in enumerate(distance_table):
        if address1 in row[0]:
            address1_row = row_index
    for col_index, col in enumerate(distance_table[0]):
        if address2 in col:
            address2_col = col_index
    if address1_row >=0 and address2_col >=0:
        return distance_table[address1_row][address2_col]
    return "Error"



def distance_from_hub(distance_table, address):
    for row in distance_table:
        if address in row[0]:
            distance = row[3]
            return distance

def closest_neighbor(address, distance_table):
    row_index = 0
    min_distance_row = 100
    min_distance_column = 100
    #determine what row address is in
    for row in distance_table:
        if address in row[0]:
            break
        row_index += 1
    print("Row index:", row_index)
    print("address:", address)

    #determine what column address is in
    column_index = 0
    for item in distance_table[0]:
        if address.strip() in item.strip():
            break
        column_index += 1

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
            distance_table.append(row)

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





