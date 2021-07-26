from compares import *

class DataInterface (ComparesInterface):
    """ An interface for the a data object to be used in the binary search tree, as an object to
        be added to the tree.

        This interface is implemented by the DataObject class in data_object.py.
    """

    def __init__ (self):
        pass

    def copy (self):
        """
        Returns a deep copy of this object.
        """

    def compare_key (self, key):
        """
        Compare this object's key to the parameter key

        Return values:
        1: This object's key is greater than the parameter key
        0: This object's key is equal to the parameter key
        -1: This object's key is less than the parameter key
        """