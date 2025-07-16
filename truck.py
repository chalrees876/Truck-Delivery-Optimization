import re


class Truck:
    def __init__(self):
        self.weight = 0
        self.miles_driven = 0
        self.packages_loaded = []
        self.current_location = "HUB"
        self.current_time = "8:00 AM"
        self.speed = 18


    def add_package(self, package):
        self.packages_loaded.append(package)
        self.weight += package.weight_kg
        package.status = "In Route"

    def deliver_package(self, package, miles_driven):
        self.packages_loaded.remove(package)
        self.current_location = package.address
        self.weight -= package.weight_kg
        self.miles_driven += miles_driven
        package.status = "Delivered"

    def calculate_time(self, miles_driven, current_time):
        if "AM" in current_time:
            match = re.match(r"^(\d{1,2}):(\d{2})", current_time)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))
            time = miles_driven / self.speed
            time = time * 60
            if time == 60:
                hour += 1
            elif time > 60:
                remainder = time % 60
                hours = round(time / 60, 0)
                hour += hours
                minute += remainder
            else:
                minute += time
            if minute == 60:
                minute = 00
                hour += 1
            elif minute > 60:
                hours += round(minute/60, 0)
                minute += minute % 60

            hour = round(hour, 0)
            minute = round(minute, 0)
            hour = int(hour)
            minute = int(minute)


            if hour < 12:
                return f'{hour}:{minute} AM'
            elif hour == 12:
                return f'{hour}:{minute} PM'
            else:
                return f'{hour - 12}:{minute} PM'







