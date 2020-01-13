import warnings

# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
    
    def __repr__(self):
        return f"{self.key} + {self.value} next:{self.next}"

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        index = self._hash_mod(key)
        head = self.storage[index]
        if head is None or head.key == key:
          head = LinkedPair(key, value)
        else:
          temp = head
          while temp.next is not None and temp.next.key != key:
            temp = temp.next
          temp.next = LinkedPair(key, value)
        self.storage[index] = head
         

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        head = self.storage[index]
        if head is None:
          warnings.warn('The key is not here!')
        elif head.key == key:
          head = None
        else:
          temp = head
          while temp.next is not None:
            if key == temp.next.key:
              temp.next = temp.next.next
            else:
              temp = temp.next
        self.storage[index] = head


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        value = None
        for i in range(0, self.capacity):
        #   if key == self.storage[i]:
        #     return 'true'
        # index = self._hash_mod(key)
          head = self.storage[i]
          if head is None:
            pass
          elif head.key == key:
            value = head.value
          else:
            while head.next is not None:
              head = head.next
              if key == head.key:
                value = head.value
        return value

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        newHash = HashTable(self.capacity * 2)
        for i in range(0,self.capacity):
          newHash.storage[i] = self.storage[i]
        self.storage = newHash.storage
        self.capacity = newHash.capacity



if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
