""" Implementation of a binary heap
   This class implements a binary heap with object elements
   The elements must implement a Compares interface, which uses
   a compare() method for element comparision, where:
     1: Object calling the method is bigger than the one used as an argument
     0: Object calling the method is equal to the one used as an argument
     -1: Object calling the method is less than the one used as an argument

   Ex) object1.compare(object2)
"""

class BinaryHeap:

    MIN_HEAP = 0
    MAX_HEAP = 1

    def __init__(self, heap_type):
        self.array = []
        self.heap_type = heap_type

    def get_size(self):
        return len(self.array)

    def get_array(self):
        return self.array

    # Determines the existence of a left child
    def left_child_exist(self, index):
        if (self.left_child(index) > len(self.array) - 1):
            return False
        else:
            return True

    # Determines the existence of a right child
    def right_child_exist(self, index):
        if self.right_child(index) > len(self.array) - 1:
            return False
        else:
            return True

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return (2 * index + 1)

    def right_child(self, index):
        return (2 * index + 2)

    def is_empty(self):
        if len(self.array) == 0:
            return True
        else:
            return False

    def heapify(self):
        if len(self.array) == 0:
            return

        index = len(self.array) - 1

        while(index >= 0):
            self.sift_down(index)
            index = index - 1

    # This method builds the heap from an array by iterating from the last element of the array to
    #   the first element of the array, and calling sift_down() on each iteration
    def build(self, array):
        if len(array) == 0:
            return

        self.array = array
        index = len(self.array) - 1

        while(index >= 0):
            self.sift_down(index)
            index = index - 1

    def add(self, value):
        index = len(self.array)
        self.array.append(value)
        self.sift_up(index)

    def pop(self):
        value = None
        if len(self.array) > 0:
            value = self.array[0]
            if len(self.array) > 1:
                self.array[0] = self.array.pop()
                self.sift_down(0)
            else:
                self.array.pop()
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
        while(index < len(self.array) and complete == False):

            # existence of children
            if(self.left_child_exist(index)):
                if(self.right_child_exist(index)):
                
                    # determine smaller/bigger value by heap type
                    if(self.heap_type == BinaryHeap.MAX_HEAP):
                        if(self.array[self.left_child(index)].compare( self.array[self.right_child(index)]) == 1):
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