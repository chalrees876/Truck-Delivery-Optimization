
class HashTable(object):
    def __init__(self, size=10):
        self.num_elements = 0
        self.data = [[] for _ in range(size)]
        self.size = len(self.data)

    def insert(self, package):
        index = package.package_id % self.size
        bucket = self.data[index]

        bucket.append(package)
        return

    def get(self, package_id):
        index = package_id % self.size
        for package in self.data[index]:
            if package_id == int(package.package_id):
                return package


    def remove(self, key):
        pass