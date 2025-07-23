import re


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
        print("Address", self.address, end=" | ")
        print("City", self.city, end=" | ")
        print("Zipcode", self.zipcode, end=" | ")
        print("Weight", self.weight_kg, end=" | ")
        print("Truck", self.truck, end=" | ")
        print("Status", self.status, end=" | ")
        print("Time Picked Up:", self.loaded_time, end=" | ")
        if self.delayed_time:
            print("Delayed Time:", self.delayed_time, end=" | ")
        print("Deadline", self.deadline, end=" | ")
        if self.status == "Delivered":
            print("Time delivered:", self.time_delivered, end=" | ")
        print("")





    def print_info_at_time(self, time):
        current_time = convert_string_time_to_int(time)
        package_delivered_time = convert_string_time_to_int(self.time_delivered)
        package_loaded_time = convert_string_time_to_int(self.loaded_time)
        #package has been delivered
        if self.package_id == 9:
            if current_time <= convert_string_time_to_int("10:20 AM"):
                self.address = "300 State St"
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84103"
        if current_time >= package_delivered_time:
            self.print_info()
            return
        #package has been loaded but not delivered
        if package_delivered_time > current_time >= package_loaded_time:
            print("---------------"
                  "Package Id", self.package_id, "Info"
                                                 "------------------")
            print("Address", self.address, end=" | ")
            print("City", self.city, end=" | ")
            print("Zipcode", self.zipcode, end=" | ")
            print("Weight", self.weight_kg, end=" | ")
            print("Truck", self.truck, end=" | ")
            print("Status", "En route", end=" | ")
            print("Time Picked Up:", self.loaded_time, end=" | ")
            print("Deadline", self.deadline, end=" | ")
            if self.delayed_time:
                print("Delayed Time:", self.delayed_time, end=" | ")
            print("")
            return
        #package has not been loaded
        else:
            print("---------------"
                  "Package Id", self.package_id, "Info"
                                                 "------------------")
            print("Address", self.address, end=" | ")
            print("City", self.city, end=" | ")
            print("Zipcode", self.zipcode, end=" | ")
            print("Weight", self.weight_kg, end=" | ")
            print("Truck", "None", end=" | ")
            if self.incorrect_address:
                if current_time <= convert_string_time_to_int("10:20 AM"):
                    print("Status", "In hub, Incorrect Address", end = " | ")
                else:
                    print("Status", "In hub, correct address", end=" | ")
            elif self.delayed_time:
                if convert_string_time_to_int(self.delayed_time) > current_time:
                    print("Status", "Not at hub yet", end = " | ")
            else:
                print("Status", "In hub", end=" | ")
            if not self.delayed_time:
                print("Deadline", self.deadline)
            else:
                print("Deadline", self.deadline, end=" | ")
                print("Delayed Time:", self.delayed_time)



