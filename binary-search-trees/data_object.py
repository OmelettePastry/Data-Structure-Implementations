from data_interface import *

class DataObject (DataInterface):
    """ Data Object

        Our sample object class used in our binary search tree demonstration. This will create an object that
        will be used as an argument in the insert() method in our binary search trees.

    """

    def __init__ (self, key):
        self.key = key

    def get_key (self):
        return self.key

    def copy (self):
        new_obj = DataObject(self.key)

        return new_obj

    def compare_key (self, key):
        if self.key > key:
            return 1
        elif self.key < key:
            return -1
        else:
            return 0

    def compare (self, object):
        if self.key > object.get_key():
            return 1
        elif self.key < object.get_key():
            return -1
        else:
            return 0