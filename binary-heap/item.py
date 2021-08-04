from compares import ComparesInterface

class Item(ComparesInterface):
    def __init__(self, value):
        self.value = value
        
    def get_value(self):
        return self.value
        
    def compare(self, object):
        result = None
        
        if (self.value > object.value):
            result = 1
        elif (self.value < object.value):
            result = -1
        else:
            result = 0
            
        return result

    def get_value(self):
        return self.value