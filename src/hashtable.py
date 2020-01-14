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
        self.original = True


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
        # DBJ2 hash in C
        # unsigned long
        # hash(unsigned char *str)
        # {
        #     unsigned long hash = 5381;
        #     int c;

        #     while (c = *str++)
        #         hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

        #     return hash;
        # }
        hash = 5381
        for x in key:
            hash = (( hash << 5) + hash) + ord(x) & 0xFFFFFFFF
        return hash

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash_djb2(key) % self.capacity


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
        self.check()
        

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
        self.check()


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        # value = None
        # for i in range(0, self.capacity):
        index = self._hash_mod(key)
        head = self.storage[index]
        if head is None:
          return None
        elif head.key == key:
          return head.value
        else:
          while head.next is not None:
            head = head.next
            if key == head.key:
              return head.value
        return None

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        newHash = HashTable(self.capacity * 2)
        for i in range(0,len(self.storage)):
          if self.storage[i] is not None:
            newHash.insert(self.storage[i].key, self.storage[i].value)
            while self.storage[i].next is not None:
              self.storage[i] = self.storage[i].next
              newHash.insert(self.storage[i].key, self.storage[i].value)
        self.storage = newHash.storage
        self.capacity = newHash.capacity
        self.original = False


    def shrink(self):
        '''
        Halves the capacity of the hash table and
        rehash all key/value pairs.
        '''
        newHash = HashTable(int(len(self.storage)/2))
        for i in range(0,len(self.storage)):
          if self.storage[i] is not None:
            newHash.insert(self.storage[i].key, self.storage[i].value)
            while self.storage[i].next is not None:
              self.storage[i] = self.storage[i].next
              newHash.insert(self.storage[i].key, self.storage[i].value)
        self.storage = newHash.storage
        self.capacity = newHash.capacity


    def check(self):
      '''
      Check if the hash should shrink or resize
      '''
      count = 0 
      for i in range(0, len(self.storage)):
        if self.storage[i] is not None:
          count += 1
      if count >= (len(self.storage)*.7):
          self.resize()
      if count <= (len(self.storage)*.2) and count >= 3 and self.original is False:
          self.shrink()

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
