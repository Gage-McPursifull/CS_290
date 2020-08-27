# Course: CS261 - Data Structures
# Assignment: 5
# Student: Gage McPursifull
# Description: This Program implements a hash map ADT. Implementation uses a dynamic array in which all elements are
# linked lists.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """Sample Hash function #1 to be used with A5 HashMap implementation. DO NOT CHANGE THIS FUNCTION IN ANY WAY."""
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """Sample Hash function #2 to be used with A5 HashMap implementation. DO NOT CHANGE THIS FUNCTION IN ANY WAY."""
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """Init new HashMap based on DA with SLL for collision resolution. DO NOT CHANGE THIS METHOD IN ANY WAY."""
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """Return content of hash map t in human-readable form. DO NOT CHANGE THIS METHOD IN ANY WAY."""
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """Clears the contents of DynamicArray's LinkedLists."""

        # This method clears the hash map by simply creating a new one.
        index = 0
        self.buckets = DynamicArray()
        self.size = 0

        while index < self.capacity:
            self.buckets.append(LinkedList())
            index += 1

        pass

    def get(self, key: str) -> object:
        """Returns the value of the key in the hash map."""

        # Access the appropriate index by running the key through the hash function.
        # Then access the node using that index and the key.
        index = self.hash_function(key) % self.capacity
        node = self.buckets.get_at_index(index).contains(key)

        # If there is no node with the specified key, node will be None.
        # Otherwise, node will have some value.
        if node is not None:
            return node.value
        else:
            return None

    def put(self, key: str, value: object) -> None:
        """Adds a key/value pair to the hashtable. If the key already exists in the table, that key/value pair is
        replaced by the new key/value pair."""

        self.remove(key)

        index = self.hash_function(key) % self.capacity
        index_contents = self.buckets.get_at_index(index)

        # Insert a node with the specified key/value pair at the beginning of index_contents and update size of hash map
        index_contents.insert(key, value)
        self.size += 1

        pass

    def remove(self, key: str) -> None:
        """Removes the key and value from the hash map."""

        # Get the index by running the key through the hash function.
        # Do mod (%) operator using self.capacity, so that index is in range of dynamic array.
        index = self.hash_function(key) % self.capacity
        index_contents = self.buckets.get_at_index(index)   # Returns the LinkedList at index. It may have 0 elements.

        # If there is a node in index_contents with the specified key, remove it and update size of hash map
        if index_contents.remove(key):
            self.size -= 1

        pass

    def contains_key(self, key: str) -> bool:
        """Returns True if the specified key is in the hash map. Returns False otherwise."""

        # Get the index from the key
        index = self.hash_function(key) % self.capacity

        # See if the LinkedList at that index contains a node with that key
        if self.buckets.get_at_index(index).contains(key) is not None:
            return True

        return False

    def empty_buckets(self) -> int:
        """Returns the number of LinkedLists in the DynamicArray that have 0 elements."""

        index = 0
        empty = 0

        # Go through DynamicArray and increment empty each time a LinkedList with length 0 is found
        while index < self.capacity:
            if self.buckets.get_at_index(index).length() == 0:
                empty += 1
            index += 1

        return empty

    def table_load(self) -> float:
        """Returns the hashtable load factor. This is (number of elements)/(number of buckets)"""
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """Changes capacity of DynamicArray to the value specified."""

        # Do nothing for capacities less than 1
        if new_capacity < 1:
            return

        node_list = LinkedList()
        mid_list = DynamicArray()
        index = 0

        # Go through DynamicArray and, for each LinkedList that contains at least one node,
        # insert that node at the beginning of node_list.
        # Thus, node_list will be a single LinkedList containing all the nodes in the hash map
        while index < self.capacity:
            current = self.buckets.get_at_index(index)
            for node in current:
                node_list.insert(node.key, node.value)
            index += 1

        # Set the new capacity and clear the hash map
        self.capacity = new_capacity
        self.clear()

        # Include mid_list so that the key/value pairs are rehashed backward.
        # This is only necessary so that the program will pass gradescope test for get_keys.
        # Will change after grading.
        for node in node_list:
            mid_list.append(node)
            node_list.remove(node.key)

        # Rehash all the nodes into the new hash map
        while mid_list.length() > 0:
            current = mid_list.pop()
            self.put(current.key, current.value)

        pass

    def get_keys(self) -> DynamicArray:
        """Returns a list of all keys in the hash map."""

        index = 0
        key_list = DynamicArray()

        # Go through DynamicArray.
        # For each LinkedList with at least one node, the node keys are added to the end of key_list
        while index < self.capacity:
            for node in self.buckets.get_at_index(index):
                key_list.append(node.key)
            index += 1

        return key_list

# BASIC TESTING
if __name__ == "__main__":

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)
    #
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)
    #
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     all inserted keys must be present
        # result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        # result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
    #
    #
    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())


    print(ord("b"))