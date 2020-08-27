# Course: CS261 - Data Structures
# Assignment: 5
# Student: Gage McPursifull
# Description: This Program implements a min heap ADT using a dynamic array as the underlying storage.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """Custom exception to be used by MinHeap class. DO NOT CHANGE THIS CLASS IN ANY WAY"""
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """Initializes a new MinHeap. DO NOT CHANGE THIS METHOD IN ANY WAY."""
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """Return MH content in human-readable form. DO NOT CHANGE THIS METHOD IN ANY WAY."""
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """Return True if no elements in the heap, False otherwise. DO NOT CHANGE THIS METHOD IN ANY WAY."""
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """Adds the value to the DynamicArray."""

        # Add the node to the end of the array. Set node_index equal to its index.
        self.heap.append(node)
        node_index = self.heap.length() - 1

        parent_index = (node_index - 1)//2

        # Keep swapping the node with its parent until the parent node is larger, or the front of the list is reached.
        while node < self.heap.get_at_index(parent_index) and parent_index >= 0:
            self.heap.swap(node_index, parent_index)
            node_index = parent_index
            parent_index = (node_index - 1)//2

        pass

    def get_min(self) -> object:
        """Get minimum value from heap. In a min heap, the first element is always the smallest."""
        if self.is_empty():
            raise MinHeapException

        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """Get and remove minimum value from heap."""

        # Empty heap has no min value
        if self.is_empty():
            raise MinHeapException

        # Get the index and value of the last node. It will replace the lead node temporarily.
        replace_index = self.heap.length() - 1
        replacement = self.heap.get_at_index(replace_index)

        # Swap the lead node with the last node.
        # Save the lead node value in mini.
        # Get the index of the replacement node's left and right children.
        self.heap.swap(0, replace_index)
        mini = self.heap.pop()
        replace_index = 0
        left_child_index = replace_index*2 + 1
        right_child_index = replace_index*2 + 2

        # If both children have indices that exceed the list bounds, we are done.
        if (left_child_index > self.heap.length() - 1) and (right_child_index > self.heap.length() - 1):
            return mini

        # If only the right_child_index exceeds the list bounds, make right_child and left_child refer to same node.
        if right_child_index > self.heap.length() - 1:
            left_child = self.heap.get_at_index(left_child_index)
            right_child = self.heap.get_at_index(left_child_index)
            right_child_index = left_child_index
        # Otherwise, get the value of left and right child.
        else:
            left_child = self.heap.get_at_index(left_child_index)
            right_child = self.heap.get_at_index(right_child_index)

        # This loop percolates the replacement node down the array until it reaches the appropriate spot.
        while replacement > left_child or replacement > right_child:
            # Swap replacement with the smaller of left child and right child and update its index
            if left_child < right_child:
                self.heap.swap(replace_index, left_child_index)
                replace_index = left_child_index
            else:
                self.heap.swap(replace_index, right_child_index)
                replace_index = right_child_index

            # Update the index of left and right child.
            left_child_index = replace_index * 2 + 1
            right_child_index = replace_index * 2 + 2

            # If both children have indices that exceed the list bounds, we are done.
            if (left_child_index > self.heap.length() - 1) and (right_child_index > self.heap.length() - 1):
                break

            # If only the right_child_index exceeds the list bounds, make right_child and left_child refer to same node.
            if right_child_index > self.heap.length() - 1:
                left_child = self.heap.get_at_index(left_child_index)
                right_child = self.heap.get_at_index(left_child_index)
                right_child_index = left_child_index
            # Otherwise, get the value of left and right child.
            else:
                left_child = self.heap.get_at_index(left_child_index)
                right_child = self.heap.get_at_index(right_child_index)

        return mini

    def build_heap(self, da: DynamicArray) -> None:
        """Takes an arbitrary array and creates a min heap representation of it."""

        self.heap = DynamicArray()
        index = 0

        # Copy da to self.heap
        while index < da.length():
            self.heap.append(da.get_at_index(index))
            index += 1

        # Index of the first non-leaf node
        index = (index - 2)//2

        # The outer loop increments backward through non-leaf nodes and defines the left and right children.
        while index >= 0:
            left_child_index = index*2 + 1
            right_child_index = index*2 + 2

            if right_child_index > self.heap.length() - 1:
                right_child_index = left_child_index

            parent_index = index
            parent = self.heap.get_at_index(parent_index)
            left_child = self.heap.get_at_index(left_child_index)
            right_child = self.heap.get_at_index(right_child_index)

            # Inner loop percolates the current parent down to its appropriate position in the list/heap
            while parent > left_child or parent > right_child:
                if left_child < right_child:
                    self.heap.swap(parent_index, left_child_index)
                    parent_index = left_child_index
                else:
                    self.heap.swap(parent_index, right_child_index)
                    parent_index = right_child_index

                left_child_index = parent_index*2 + 1
                right_child_index = parent_index*2 + 2

                if (left_child_index > self.heap.length() - 1) and (right_child_index > self.heap.length() - 1):
                    break

                # If only right_child_index exceeds the list bounds, make right_child and left_child refer to same node.
                if right_child_index > self.heap.length() - 1:
                    left_child = self.heap.get_at_index(left_child_index)
                    right_child = self.heap.get_at_index(left_child_index)
                    right_child_index = left_child_index
                # Otherwise, get the value of left and right child.
                else:
                    left_child = self.heap.get_at_index(left_child_index)
                    right_child = self.heap.get_at_index(right_child_index)

            # Go backward one node for the outer loop
            index -= 1

        pass
