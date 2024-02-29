
class HashTable:
    # Stores data about Hash Table object
    def __init__(self, initialCapacity=40):
        self.capacity = initialCapacity
        self.size = 0 # Current size of the hash table
        self.table = [[] for _ in range(self.capacity)]

    # Custom hash function based on package ID
    def _hash(self, packageID):
        return hash(packageID)

    # Resize function for hash table
    def _resize(self):
        self.capacity *= 2
        newTable = [[] for _ in range(self.capacity)]
        for bucket in self.table:
            for packageID, data in bucket:
                newBucketIndex = self._hash(packageID) % self.capacity
                newTable[newBucketIndex].append([packageID, data])
        self.table = newTable

    # Insert new item then update item if in already in list
    def insert(self, key, item):
        if self.size / self.capacity > 0.7:
            self._resize()
        bucketIndex = self._hash(key) % self.capacity
        bucket = self.table[bucketIndex]
        for kv in bucket:
            if kv[0] == key:
                kv[1] = item
                return
        bucket.append([key, item])
        self.size += 1
        
    # Search for item with matching key
    def search(self, key):
        bucketIndex = self._hash(key) % self.capacity
        bucket = self.table[bucketIndex]
        for kv in bucket:
            if kv[0] == key:
                return kv[1]
        return None
    
    def setTrucksToPackages(self, list_of_trucks, list_of_num_of_truck):
        for i, truck in enumerate(list_of_trucks):
            for package in truck.packages:
                package = self.search(package)
                package.truck = list_of_num_of_truck[i]