
class HashTable(object):
    def __init__(self, size=10):
        self.num_elements = 0
        self.data = [[] for _ in range(size)]
        self.size = len(self.data)

    def insert(self, package):
        index = package.package_id % self.size
        bucket = self.data[index]
        self.num_elements += 1

        bucket.append(package)
        return

    def get(self, package_id):
        index = package_id % self.size
        for package in self.data[index]:
            if package_id == int(package.package_id):
                return package
        print("Package", package_id, "Not found")
        return None

    def get_all(self):
        num_printed = 0
        i = 1
        while num_printed < self.num_elements:
            package = self.get(i)
            if package is not None:
                package.print_info()
                num_printed += 1
                i += 1
            else:
                i += 1





    def remove(self, package_id):
        index = package_id % self.size
        bucket = self.data[index]
        for package in self.data[index]:
            bucket_index = 0
            if package_id == int(package.package_id):
                print("removing package", package.package_id)
                self.num_elements -= 1
                bucket.pop(bucket_index)
            else:
                bucket_index += 1
        return "Bucket not found"