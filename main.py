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

    truck_distance_table(truck1, distance_table)

    for package in truck1.packages_loaded:
        package.print_info()

    truck1_packages = truck1.packages_loaded

    truck1.deliver_package(truck1_packages[0])

    print(truck1_packages)
    print(truck1.current_location)
    print(truck1.miles_driven)


    closest_neighbor(hashtable.get(13).address, distance_table)





def truck_distance_table(truck, distance_table):
    truck_table = []
    for package in truck.packages_loaded:
        for row in distance_table:
            if package.address in row[0]:
                print(package.address)
                print("PACKAGE ADDRESS IN row[0]", row[1])





def closest_neighbor(address, distance_table):
    row_index = 0
    column_index = 0
    for row in distance_table:
        if address not in row[1]:
            row_index += 1
        else:
            break
    address_row = distance_table[row_index]
    for row in distance_table:
        pass



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





