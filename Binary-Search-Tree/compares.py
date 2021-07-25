

class ComparesInterface:
    """ An interface for objects to compare other objects.

        This interface is used by the DataInterface interface in data_interface.py.
    """

    def __init__ (self):
        pass

    def compare (self, object):
        """
        Compare this object to the the parameter object.

        Return values:
        1: This object is greater than the parameter object.
        0: This object is equal to the parameter object.
        -1: This object is less than the parameter object.
        """