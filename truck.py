class Truck:
    def __init__(self):
        self.weight = 0
        self.miles_driven = 0
        self.packages_loaded = []
        self.current_location = "HUB"


    def add_package(self, package):
        self.packages_loaded.append(package)
        self.weight += package.weight_kg

    def deliver_package(self, package):
        self.packages_loaded.remove(package)
        self.current_location = package.address
        self.weight -= package.weight_kg



