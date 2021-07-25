from binary_search_tree import *        # We will create a class that will inherit BinarySearchTree

"""
Module for RedBlackNode and RedBlackTree class.

Classes:
RedBlackNode - Class for a node to be used in a red-black tree
RedBlackTree - Class for a red-black tree implementation
"""

class RedBlackNode(Node):
    """
    This class is used to create a red-black node object that is to be used in a red-black tree. 
    This class inherits from the 'Node' class. This class adds the 'self.color' variable. The
    class' constructor extends the parent constructor. The copy() method overrides the parent's
    copy() method. 

    NIL nodes are designated by having 'None' in the 'data' variable, and its 'color' variable should
    be initialized with 'Node.BLACK'

    Public methods:
    __init__  -- [EXTENDS] constructor
    copy      -- [OVERRIDES] create deep copy of the node
    set_color -- sets the color of the node
    get_color -- gets the color of the node
    * This class inherits all other class methods from the parent class

    Instance variables:
    self.color  -- color of the node
    * This class inherits all other instance variables from the parent class

    Class data members:
    BLACK       -- Designates a node to be black
    RED         -- Designates a node to be red
    (LEFT)      -- Designates a node to be left
    (RIGHT)     -- Designates a node to be right

    Constructor:
    __init__  -- The constructor extends the parent constructor. The parent constructor is called 
                 and then sets its color variable. The user is responsible for setting the color 
                 of the red-black node upon its creation, in the case of creating a new node (RED) 
                 or a nil node (BLACK).
    """
    BLACK = "Black"
    RED = "Red"

    def __init__ (self, data, parent, color):
        super().__init__(data, parent)
        self.color = color

        if data != None:
            self.left_child = RedBlackNode(None, self, RedBlackNode.BLACK)
            self.right_child = RedBlackNode(None, self, RedBlackNode.BLACK)

    def copy (self):
        """
        Create a deep copy of the object and returns a reference to it. Overrides the copy() 
        method in the parent class. Override is required as a 'RedBlackNode' instead of 'Node' 
        object is needed for the copy.

        Return value:
        A reference to a deep copy of this object
        """

        if self.data != None:
            new_node = RedBlackNode(self.data.copy(), None, self.color)
            new_node.set_count(self.count)
        else:
            new_node = None

        return new_node

    def set_color (self, color):
        """
        Sets the color of the node.
        
        Keyword arguments:
        color -- the color of the node (values are the member variables of this class)
        """
        self.color = color

    def get_color (self):
        """
        Returns the color of the node
        
        Return value:
        The color of the node
        """
        return self.color

class RedBlackTree(BinarySearchTree):
    """
    This class implements a red-black tree, inheriting from BinarySearchTree. This class uses some of 
    the methods from its parent class and also overrides and extends some of its methods.

    Operations:
    INSERT - This class overrides the insert() method. A call to the insert_node() parent method is 
             called, passing a RedBlackNode object (instead of a Node object in the parent class).
             After a normal insertion, insert_balance() is called to balance the tree.

    DELETE - This class uses the delete() method from the parent class. The delete() method from the 
             parent class will call delete_node(), which in this case will be the method here that
             overrides the parent method. Additional methods will be used to delete a red-black node 
             from the tree and rebalance it.

    Public methods:
    __init__              -- [EXTENDS] constructor
    roate_left            -- does a left rotation on the node
    rotate_right          -- does a right rotation on the node
    insert                -- [OVERRIDES] inserts data object into the tree via inside a red-black node
    insert_balance        -- balances the tree after an insertion
    delete_node           -- [OVERRIDES] deletes a node    
    delete_zero_childreen -- deletes a node with zero children
    delete_one_children   -- deletes a node with one children
    delete_two_children   -- deletes a node with two children    
    case_0                -- Case 0 of rebalancing/recoloring
    case_1                -- Case 1 of rebalancing/recoloring
    case_2                -- Case 2 of rebalancing/recoloring
    case_3                -- Case 3 of rebalancing/recoloring
    case_4                -- Case 4 of rebalancing/recoloring    

    * This class inherits all other methods from the parent class

    Instance variables:
    * This class inherits all instance variables from the parent class

    Constructor:
    __init__ -- The constructor extends the parent constructor
    """

    def __init__ (self):
        """ Constructor """
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

    """ INSERT METHODS"""

    def insert_balance (self, z_node):
        """
        Balance the tree after insertion
        
        Keyword arguments:
        z_node -- the node that was inserted
        """
        
        # If the inserted node is the root, color it black
        if z_node.get_parent() == None:
            z_node.set_color(RedBlackNode.BLACK)

        else:
            if z_node.get_parent().get_color() == RedBlackNode.RED:

                uncle = z_node.get_uncle()
                parent = z_node.get_parent()
                grandparent = parent.get_parent()
                child_side = z_node.child_side()
                parent_child_side = parent.child_side()

                if uncle.get_color() == RedBlackNode.RED:

                    parent.set_color(RedBlackNode.BLACK)
                    grandparent.set_color(RedBlackNode.RED)
                    uncle.set_color(RedBlackNode.BLACK)

                    self.insert_balance(grandparent)

                elif uncle.get_color() == RedBlackNode.BLACK:

                    if ((child_side == RedBlackNode.LEFT) and (parent_child_side == RedBlackNode.RIGHT)) or \
                       ((child_side == RedBlackNode.RIGHT) and (parent_child_side == RedBlackNode.LEFT)):

                        if child_side == RedBlackNode.LEFT:
                            self.rotate_right(parent)
                        else:
                            self.rotate_left(parent)

                        self.insert_balance(parent)

                    else:

                        if (child_side == RedBlackNode.RIGHT):
                            self.rotate_left(grandparent)
                        else:
                            self.rotate_right(grandparent)

                        parent.set_color(RedBlackNode.BLACK)
                        grandparent.set_color(RedBlackNode.RED)

    def insert (self, data):
        """
        Inserts data into the tree. This method is called to insert a data object into the tree.

        Keyword arguments:
        data -- data object (implementing DataInterface) to be inserted into the tree
        """

        # Insert the node into the tree
        node = super().insert_node(RedBlackNode(data, None, RedBlackNode.RED))

        # Balance the tree
        self.insert_balance(node)

    def delete_node(self, node):
        """
        Deletes a node and rebalances the tree. This method is called from the parent's delete() method.

        Keyword arguments:
        node -- node to be deleted
        """

        """
        Initial Steps - #1
        Determine node's replacement and x node
        """

        # Node has no children
        if node.get_left_child().is_nil() and node.get_right_child().is_nil():
            x_node = self.delete_zero_children(node)
            replacement = x_node

            if x_node == None:
                return 0

        # Node has two children
        elif (not node.get_left_child().is_nil()) and (not node.get_right_child().is_nil()):
            x_node, replacement = self.delete_two_children(node)

        # Node has one children
        else:
            x_node = self.delete_one_children(node)
            replacement = x_node

        """
        Initial Steps - #2
        Determine deleted node's color and replacement color
        """

        if (node.get_color() == RedBlackNode.RED) and (replacement.is_nil() or replacement.get_color() == RedBlackNode.RED):
            return
        elif (node.get_color() == RedBlackNode.BLACK) and (replacement.get_color() == RedBlackNode.RED):
            replacement.set_color(RedBlackNode.BLACK)
            return
        elif (node.get_color() == RedBlackNode.RED) and (replacement.get_color() == RedBlackNode.BLACK):
            replacement.set_color(RedBlackNode.RED)
        # 4th condition is a black deleted node and NIL or black replacement, in which we continue to the appropriate case

        # Let w be x's sibling
        w_node = x_node.get_sibling()

        """
        Determine case
        Case will be determined within method. A false return value indicates case is not satisfied.
        """

        if (self.case_0(x_node)):
            pass
        elif (self.case_1(x_node, w_node)):
            pass
        elif (self.case_2(x_node, w_node)):
            pass
        elif (self.case_3(x_node, w_node)):
            pass
        elif (self.case_4(x_node, w_node)):
            pass

        return 0

    """ DELETE METHODS """

    """ Deleting nodes based on number of children """

    def delete_zero_children (self, node):
        """
        Delete a node that has zero children
        
        Keyword arguments:
        node -- the node to be deleted

        Return value:
        The replacement node (node's right child [NIL child])
        """

        parent_node = node.get_parent()

        node.get_right_child().set_parent(parent_node)

        if parent_node == None:
            self.root = None
            return None

        else:
            if node.child_side() == RedBlackNode.LEFT:

                # In accordance with delete_two_children method for x_node
                parent_node.set_left_child(node.get_right_child())
            else:             
                parent_node.set_right_child(node.get_right_child())

        return node.get_right_child()

    def delete_one_children (self, node):
        """
        Delete a node that has one children
        
        Keyword arguments:
        node -- the node to be deleted

        Return value:
        the replacement node (node's child node)
        """

        parent_node = node.get_parent()

        if not node.get_left_child().is_nil():
            child_node = node.get_left_child()
        else:
            child_node = node.get_right_child()

        child_node.set_parent(parent_node)

        if parent_node == None:
            self.root = child_node

        else:

            if node.child_side() == RedBlackNode.LEFT:
                parent_node.set_left_child(child_node)
            else:
                parent_node.set_right_child(child_node)

        x_node = child_node

        return x_node

    def delete_two_children (self, node):
        """
        Delete a node that has two children
        
        Keyword arguments:
        node -- the node to be deleted

        Return value:
        value 1: the node's replacement's right child
        value 2: the replacement node (node's inorder successor)
        """

        # Store parent and child node objects
        parent_node = node.get_parent()
        node_left_child = node.get_left_child()
        node_right_child = node.get_right_child()

        # Get inorder predecessor and make a copy
        inorder_successor = node.in_order_successor()
        x_node = inorder_successor.get_right_child()
        new_node = inorder_successor.copy()

        # Set new node's parent node to point to parent, and children node to point to children
        new_node.set_parent(parent_node)
        new_node.set_left_child(node_left_child)
        new_node.set_right_child(node_right_child)

        if parent_node == None:
            self.root = new_node

        else:
            if (node.child_side() == RedBlackNode.LEFT):
                parent_node.set_left_child(new_node)
            else:
                parent_node.set_right_child(new_node)

        node_left_child.set_parent(new_node)
        node_right_child.set_parent(new_node)

        if (inorder_successor.get_left_child().is_nil()) and (inorder_successor.get_right_child().is_nil()):
            self.delete_zero_children(inorder_successor)
        else:

            self.delete_one_children(inorder_successor)

        return x_node, new_node        

    """ DELETE - BALANCE CASES """

    """
    The cases for balancing. The method parameter 'x_node' is the same x_node returned by the 
    delete-by-children methods. w_node is x_node's sibling.
    """

    def case_0 (self, x_node):
        """
        Deletion - Rebalancing and recoloring - Case 0
        
        Keyword arguments:
        x_node -- the 'x_node' returned from one of the three delete-by-children methods
        """

        if x_node.get_color() == RedBlackNode.RED:
            x_node.set_color(RedBlackNode.BLACK)
            return True
        else:
            return False

    def case_1 (self, x_node, w_node):
        """
        Deletion - Rebalancing and recoloring - Case 1
        
        Keyword arguments:
        x_node -- the 'x_node' returned from one of the three delete-by-children methods
        w_node -- x_node's sibling
        """

        if (x_node.get_color() == RedBlackNode.BLACK) and (w_node.get_color() == RedBlackNode.RED):
            w_node.set_color(RedBlackNode.BLACK)
            x_node.get_parent().set_color(RedBlackNode.RED)

            if (x_node.child_side() == RedBlackNode.LEFT):
                self.rotate_left(x_node.get_parent())
            else:
                self.rotate_right(x_node.get_parent())

            if (x_node.child_side() == RedBlackNode.LEFT):
                w_node = x_node.get_parent().get_right_child()
            else:
                w_node = x_node.get_parent().get_left_child()

            """ Determine case """

            if (self.case_2(x_node, w_node)):
                pass
            elif (self.case_3(x_node, w_node)):
                pass
            elif (self.case_4(x_node, w_node)):
                pass

            return True
        else:

            return False

    def case_2 (self, x_node, w_node):
        """
        Deletion - Rebalancing and recoloring - Case 2
        
        Keyword arguments:
        x_node -- the 'x_node' returned from one of the three delete-by-children methods
        w_node -- x_node's sibling        
        """

        if (x_node.get_color() == RedBlackNode.BLACK) and (w_node.get_color() == RedBlackNode.BLACK) and \
           (w_node.get_left_child().get_color() == RedBlackNode.BLACK) and (w_node.get_right_child().get_color() == RedBlackNode.BLACK):
    
            w_node.set_color(RedBlackNode.RED)
            x_node = x_node.get_parent()
            w_node = x_node.get_sibling()

            # print("w node color:", w_node.get_color())

            if (x_node.get_color() == RedBlackNode.RED):
                x_node.set_color(RedBlackNode.BLACK)
                return True
            else:

                """ Determine case """

                # !!! If x_node is the root and has no sibling ? ? ?
                if x_node.get_parent() == None:
                    return
                elif (self.case_1(x_node, w_node)):
                    pass
                elif (self.case_2(x_node, w_node)):
                    pass
                elif (self.case_3(x_node, w_node)):
                    pass
                elif (self.case_4(x_node, w_node)):
                    pass

            return True
        else:
            return False

    def case_3 (self, x_node, w_node):
        """
        Deletion - Rebalancing and recoloring - Case 3
        
        Keyword arguments:
        x_node -- the 'x_node' returned from one of the three delete-by-children methods
        w_node -- x_node's sibling        
        """

        x_side = x_node.child_side()
        
        if (x_node.get_color() == RedBlackNode.BLACK) and (w_node.get_color() == RedBlackNode.BLACK) and \
           ((x_side == RedBlackNode.LEFT and w_node.get_left_child().get_color() == RedBlackNode.RED and w_node.get_right_child().get_color() == RedBlackNode.BLACK) or \
           (x_side == RedBlackNode.RIGHT and w_node.get_right_child().get_color() == RedBlackNode.RED and w_node.get_left_child().get_color() == RedBlackNode.BLACK)):

            if (x_side == RedBlackNode.LEFT):
                w_node.get_left_child().set_color(RedBlackNode.BLACK)
                w_node.set_color(RedBlackNode.RED)
                self.rotate_right(w_node)
            else:
                w_node.get_right_child().set_color(RedBlackNode.BLACK)
                w_node.set_color(RedBlackNode.RED)
                self.rotate_left(w_node)

            if (x_node.child_side() == RedBlackNode.LEFT):
                w_node = x_node.get_parent().get_right_child()
            else:
                w_node = x_node.get_parent().get_left_child()

            # Move to case 4
            self.case_4(x_node, w_node)

            return True

        else:
            return False

    def case_4 (self, x_node, w_node):
        """
        Deletion - Rebalancing and recoloring - Case 4
        
        Keyword arguments:
        x_node -- the 'x_node' returned from one of the three delete-by-children methods
        w_node -- x_node's sibling        
        """
    
        if (x_node.get_color() == RedBlackNode.BLACK) and \
           ((x_node.child_side() == RedBlackNode.LEFT and w_node.get_right_child().get_color() == RedBlackNode.RED) or \
           (x_node.child_side() == RedBlackNode.RIGHT and w_node.get_left_child().get_color() == RedBlackNode.RED)):

            w_node.set_color(x_node.get_parent().get_color())
            x_node.get_parent().set_color(RedBlackNode.BLACK)

            x_side = x_node.child_side()

            if (x_side == RedBlackNode.LEFT):
               w_node.get_right_child().set_color(RedBlackNode.BLACK)
               self.rotate_left(x_node.get_parent())
            else:
               w_node.get_left_child().set_color(RedBlackNode.BLACK)
               self.rotate_right(x_node.get_parent())

            # We are done
            return True
        else:
            return False

    def get_string(self):
        """ Generates a text output of the tree using breadth first search """

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
                current_color = str(node.get_color())

                if level > 0:
                    current_parent_key = str(node.get_parent().get_key())
                
                if new_line_string == "":
                    new_line_string = new_line_string + current_key_string + "[" + current_color + "]{P = " + current_parent_key + "}(" + current_count + ")" + ":"
                else:
                    new_line_string = new_line_string + ", " + current_key_string + "[" + current_color + "]{P = " + current_parent_key + "}(" + current_count + ")" + ":"
            
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