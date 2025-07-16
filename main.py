#C950 TASK 2

#By Chris McKenzie
#Student i = 012340722



import csv
import re

from Package import Package
from hash import HashTable

def main():

    #Call function to add all packages in csv into hash table.
    hashtable = hash_packages("Resources/packages.csv")

    hashtable.get(3)
    hashtable.get(6)
    hashtable.get(14)


def hash_packages(packages_file):

    #Create empty hashtable
    hashtable = HashTable()

    with open(packages_file, mode='r') as file:
        for row in csv.reader(file):
            """Create packages for each row in the csv file."""
            package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
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





