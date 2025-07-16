import re


class Truck:
    def __init__(self, number):
        self.weight = 0
        self.miles_driven = 0
        self.packages_loaded = []
        self.current_location = "HUB"
        self.current_time = "8:00 AM"
        self.speed = 18
        self.number = number



    def add_package(self, package):
        self.packages_loaded.append(package)
        self.weight += package.weight_kg
        package.status = "In Route"
        package.truck = self.number

    def deliver_package(self, package, distance):
        self.packages_loaded.remove(package)
        self.current_location = package.address
        self.weight -= package.weight_kg
        self.miles_driven += distance
        package.status = "Delivered"
        self.current_time = self.calculate_time(distance, self.current_time)
        package.time_delivered = self.current_time

    def calculate_time(self, miles_driven, current_time):
        # Parse current time
        match = re.match(r"^(\d{1,2}):(\d{2}) (AM|PM)$", current_time.strip())
        if not match:
            raise ValueError(f"Invalid time format: {current_time}")

        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3)

        # Convert to minutes since midnight
        total_minutes = hour % 12 * 60 + minute
        if period == "PM":
            total_minutes += 12 * 60

        # Add travel time in minutes
        travel_minutes = int((miles_driven / self.speed) * 60)
        total_minutes += travel_minutes

        # Convert back to hour, minute, and AM/PM
        new_hour_24 = total_minutes // 60
        new_minute = total_minutes % 60

        period = "AM" if new_hour_24 < 12 or new_hour_24 == 24 else "PM"
        new_hour = new_hour_24 % 12
        if new_hour == 0:
            new_hour = 12

        return f"{new_hour}:{new_minute:02d} {period}"







