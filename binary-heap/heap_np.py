""" Implementation of a binary heap
   This class implements a binary heap with object elements.
   This implementation uses numpy arrays.
   
   The elements must implement a Compares interface, which uses a cpmpares() method, where:
     1: Object calling the method is bigger than the one used as an argument
     0: Object calling the method is equal to the one used as an argument
     -1: Object calling the method is less than the one used as an argument

   Ex) object1.compare(object2)
"""

import numpy as np

class BinaryHeap:

    MIN_HEAP = 0 
    MAX_HEAP = 1

    def __init__(self, heap_type):

        # Array will doube in size if full
        self.array = np.empty(8, dtype='object')

        # Keep track of number of items in array
        self.num_elements = 0
        
        self.heap_type = heap_type

    # Number of actual elements in the heap
    def get_length(self):
        return self.num_elements

    # Array size used for heap (number of proper items may be lower)
    def get_size(self):
        return self.array.size

    def get_array(self):
        return self.array

    # Determines the existence of a left child
    def left_child_exist(self, index):
        if (self.left_child(index) > self.num_elements - 1):
            return False
        else:
            return True

    # Determines the existence of a right child
    def right_child_exist(self, index):
        if self.right_child(index) > self.num_elements - 1:
            return False
        else:
            return True

    # Node parent/child calculations
    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return (2 * index + 1)

    def right_child(self, index):
        return (2 * index + 2)

    def is_empty(self):
        if self.num_elements == 0:
            return True
        else:
            return False

    def heapify (self):
        """ Organizes the array elements into a binary heap. """
        if self.num_elements == 0:
            return

        index = self.num_elements - 1

        while(index >= 0):
            self.sift_down(index)
            index = index - 1        

    def build(self, array):
        """ This method builds the heap from an array by iterating from the last element of the array to
        the first element of the array, calling sift_down() on each iteration. The 'array' argument 
        must be a numpy array of type 'object'. """

        if array.size == 0:
            return

        self.array = array

        # The array passed in the argument must be full (num elements in array must equal array.size)
        self.num_elements = self.array.size
        
        self.heapify()

    def add(self, value):
        if self.num_elements == self.array.size:
            if self.num_elements == 0:
                np.resize(self.array, 2)
            else:
                new_size = self.array.size * 2
                self.array = np.resize(self.array, int(new_size))

        self.array[self.num_elements] = value
        self.sift_up(self.num_elements)
        self.num_elements = self.num_elements + 1

    def pop(self):
        value = None
        if self.num_elements > 0:
            value = self.array[0]
            if self.array.size > 1:
                self.array[0] = self.array[self.num_elements - 1]
                self.num_elements = self.num_elements - 1
                self.sift_down(0)
            else:
                self.num_elements = self.num_elements - 1
        return value

    def swap_elements(self, x, y):
        temp = self.array[x]
        self.array[x] = self.array[y]
        self.array[y] = temp

    def sift_up(self, index):
        complete = False

        while (index > 0 and complete == False):
            parent_index = self.parent(index)
            if(self.heap_type == BinaryHeap.MAX_HEAP):
                if(self.array[index].compare(self.array[parent_index]) == 1):
                    self.swap_elements(index, parent_index)
                    index = parent_index
                else:
                    complete = True
            elif(self.heap_type == BinaryHeap.MIN_HEAP):
                if(self.array[index].compare(self.array[parent_index]) == -1):
                    self.swap_elements(index, parent_index)
                    index = parent_index
                else:
                    complete = True

    def sift_down(self, index):
        complete = False
        z_index = -1
        while(index < self.num_elements and complete == False):

            # existence of children
            if(self.left_child_exist(index)):
                if(self.right_child_exist(index)):
                
                    # determine smaller/bigger value by heap type
                    if(self.heap_type == BinaryHeap.MAX_HEAP):
                        if(self.array[self.left_child(index)].compare(self.array[self.right_child(index)]) == 1):
                            z_index = self.left_child(index)
                        else:
                            z_index = self.right_child(index)
                    elif(self.heap_type == BinaryHeap.MIN_HEAP):
                        if(self.array[self.left_child(index)].compare(self.array[self.right_child(index)]) == -1):
                            z_index = self.left_child(index)
                        else:
                            z_index = self.right_child(index)

                # only left child exist, use this value to compare with parent
                else:
                    z_index = self.left_child(index)

                # Swap if necessary, depending on heap type
                if(self.heap_type == BinaryHeap.MAX_HEAP):
                    if(self.array[z_index].compare(self.array[index]) == 1):
                        self.swap_elements(z_index, index)
                        index = z_index
                    else:
                        complete = True
                if(self.heap_type == BinaryHeap.MIN_HEAP):
                    if(self.array[z_index].compare(self.array[index]) == -1):
                        self.swap_elements(z_index, index)
                        index = z_index
                    else:
                        complete = True

            # No child exists, therefore exit loop
            else:
                complete = True