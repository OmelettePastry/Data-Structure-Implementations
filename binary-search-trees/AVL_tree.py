from binary_search_tree import *

class AVLNode(Node):

    def __init__ (self, data, parent):
        super().__init__(data, parent)

        if data != None:
            self.height = 1
            self.left_child = AVLNode(None, self)
            self.right_child = AVLNode(None, self)            
        else:
            self.height = 0
            self.left_child = None
            self.right_child = None

    def get_height (self):
        return self.height

    def set_height (self, height):
        self.height = height

    def get_sub_height (self):

        # if node's children are both not NIL
        if (not self.left_child.is_nil()) and (not self.left_child.is_nil()):

            # left child's height is larger than right child's height
            if self.left_child.get_height() > self.right_child.get_height():
                return self.left_child.get_height()

            # right child's height is larger than left child's height
            else:
                return self.right_child.get_height()
        
        # node only has left child, return left child's height
        elif not self.left_child.is_nil():
            return self.left_child.get_height()
        
        # node onlu has right child, return right child's height
        elif not self.right_child.is_nil():
            return self.right_child.get_height()
        
        else:
            return 0

    def calc_height (self):
        self.height = 1 + self.get_sub_height()

class AVLTree(BinarySearchTree):

    LEFT_LEFT = "Left-Left"
    LEFT_RIGHT = "Left-Right"
    RIGHT_LEFT = "Right-Left"
    RIGHT_RIGHT = "Right-Right"    

    def __init__ (self):
        super().__init__()

    def rotate_left (self, node):
        """
        Rotates the node left.
        
        Keyword arguments:
        node -- the node to rotate
        """

        y_node = node.get_right_child()
        y_child = y_node.get_left_child()        

        # Set y's new parent to current node's parent
        y_node.set_parent(node.get_parent())

        # Set y's new parent's left or right child to y
        if y_node.get_parent() == None:
            self.root = y_node
        else:

            # Determine which side the current node was originally at
            if node.child_side() == Node.LEFT:
                y_node.get_parent().set_left_child(y_node)
            else:
                y_node.get_parent().set_right_child(y_node)

        # Set y's left child to original node
        y_node.set_left_child(node)

        # Set original node's parent to y
        node.set_parent(y_node)

        # Set original node's right child to y's left child
        node.set_right_child(y_child)

        # Set original node's new right child's parent to the original node
        node.get_right_child().set_parent(node)

        # Calculate height of node (now below y_node)
        node.calc_height()

        # Then calculate height of y_node
        y_node.calc_height() 

    def rotate_right (self, node):
        """
        Rotate node right
        
        Keyword arguments:
        node -- the node to rotate
        """

        y_node = node.get_left_child()
        y_child = y_node.get_right_child()

        # Set y's new parent to current node's parent
        y_node.set_parent(node.get_parent())

        # Set y's new parent's left or right child to y
        if y_node.get_parent() == None:
            self.root = y_node
        else:

            # Determine which side the current node was originally at
            if node.child_side() == Node.LEFT:
                y_node.get_parent().set_left_child(y_node)
            else:
                y_node.get_parent().set_right_child(y_node)

        # Set y's right child to original node
        y_node.set_right_child(node)

        # Set original node's parent to y
        node.set_parent(y_node)

        # Set original node's left child to y's right child
        node.set_left_child(y_child)

        # Set original node's new left child's parent to the original node
        node.get_left_child().set_parent(node)

        # Calculate height of node (now below y_node)
        node.calc_height()

        # Then calculate height of y_node        
        y_node.calc_height()

    def insert (self, data):
        node = super().insert_node(AVLNode(data, None))

        self.rebalance(node)

    def balance_case (self, node):

        if node.is_nil() or (node.get_left_child().is_nil() and node.get_right_child().is_nil()):
            return None

        left_child = node.get_left_child()
        right_child = node.get_right_child()  

        # left child has the bigger height
        if (left_child.get_height() - right_child.get_height()) > 1:

            # left child's left child has bigger height
            if left_child.get_left_child().get_height() > left_child.get_right_child().get_height():
                return AVLTree.LEFT_LEFT

            # left child's right child has bigger height
            else:
                return AVLTree.LEFT_RIGHT

        # right child has bigger height
        elif (left_child.get_height() - right_child.get_height()) < -1:

            # right child's left child has bigger height
            if right_child.get_left_child().get_height() > right_child.get_right_child().get_height():
                return AVLTree.RIGHT_LEFT

            # right child's right child has bigger height
            else:
                return AVLTree.RIGHT_RIGHT

        return None

    def rebalance (self, node):

        node = node.get_parent()

        while node != None:

            # set current node's height to 1 + max height of child trees
            node.set_height(node.get_sub_height() + 1)

            # tree structure cases
            if (self.balance_case(node) == AVLTree.LEFT_LEFT):
                self.rotate_right(node)
                node = node.get_parent()

            elif (self.balance_case(node) == AVLTree.LEFT_RIGHT):
                self.rotate_left(node.get_left_child())
                self.rotate_right(node)
                node = node.get_parent()

            elif (self.balance_case(node) == AVLTree.RIGHT_LEFT):
                self.rotate_right(node.get_right_child())
                self.rotate_left(node)
                node = node.get_parent()

            elif (self.balance_case(node) == AVLTree.RIGHT_RIGHT):
                self.rotate_left(node)
                node = node.get_parent()

            # go up the tree
            node = node.get_parent()

    def get_string(self):
        """ Generates a text output of the tree """

        output_string = ""
        queue = []
        level = 0

        queue.append(self.root)

        if self.root == None:
            output_string = "[None]"
            return output_string

        while (len(queue) != 0):
            original_length = len(queue)
            new_line_string = ""
            current_parent_key = "None"

            for i in range(original_length):
                
                node = queue.pop()
                current_key_string = str(node.get_key())
                current_count = str(node.get_count())

                if level > 0:
                    current_parent_key = str(node.get_parent().get_key())
                
                if new_line_string == "":
                    new_line_string = new_line_string + current_key_string + "{P = " + current_parent_key + "}{H = " + str(node.get_height()) + "}(" + current_count + ")" + ":"
                else:
                    new_line_string = new_line_string + ", " + current_key_string + "{P = " + current_parent_key + "}{H = " + str(node.get_height()) + "}(" + current_count + ")" + ":"
            
                if not node.get_left_child().is_nil():
                    new_line_string = new_line_string + "[" + str(node.get_left_child().get_key()) + "]"
                    queue.insert(0, node.get_left_child())
                else:
                    new_line_string = new_line_string + "[None]"
                if not node.get_right_child().is_nil():
                    new_line_string = new_line_string + "[" + str(node.get_right_child().get_key()) + "]"
                    queue.insert(0, node.get_right_child())
                else:
                    new_line_string = new_line_string + "[None]"

            output_string = output_string + "\n=== LEVEL " + str(level) + " ===\n"
            output_string = output_string + new_line_string + "\n"

            level = level + 1

        return output_string