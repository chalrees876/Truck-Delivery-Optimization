class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight_kg):
        self.weight_kg = weight_kg
        self.deadline = deadline
        self.zipcode = zipcode
        self.state = state
        self.city = city
        self.address = address
        self.package_id = package_id
        self.status = "In hub"
        self.truck = None
        self.delayed_time = None
        self.incorrect_address = False
        self.delivered_with = []
        self.time_delivered = ""
        self.loaded_time = ""

    def deliver(self):
        self.status = "Delivered"

    def print_info(self):
        print("---------------"
              "Package Id", self.package_id, "Info"
                "------------------")
        print("Address", self.address)
        print("City", self.city)
        print("Zipcode", self.zipcode)
        print("Deadline", self.deadline)
        print("Weight", self.weight_kg)
        print("Status", self.status)
        print("Truck", self.truck)
        if self.status == "Delivered":
            print("Time delivered:", self.time_delivered)
        if self.delayed_time:
            print("Delayed Time:", self.delayed_time)
        print("Delivered with:", self.delivered_with)
        print("Time Picked Up:", self.loaded_time)




