class Node:

    LEFT = "Left"
    RIGHT = "Right"

    def __init__ (self, data, parent):
        self.data = data
        self.parent = parent

        # If this is a non-NIL Node
        if data != None:
            self.count = 1
            self.left_child = Node(None, self)
            self.right_child = Node(None, self)

        # NIL node
        else:
            self.count = 0
            self.left_child = None
            self.right_child = None

    def copy (self):
        """
        Creates a deep copy of the node. For the new node, the 'data' and 'count' members will 
        be copied. The parent will be 'None' and children will be NIL nodes.
        """
        
        # Copy only non-NIL nodes
        if self.data != None:
            new_node = Node(self.data.copy(), None)
            new_node.set_count(self.count)
        else:
            new_node = None

        return new_node

    def set_left_child (self, left_child):

        # Set left child only if this node is non-NIL
        if self.data != None:
            self.left_child = left_child

    def set_right_child (self, right_child):

        # Set right child only if this node is non-NIL
        if self.data != None:
            self.right_child = right_child

    def set_parent (self, parent):

        self.parent = parent

    def set_data (self, data):

        self.data = data

    def set_count (self, count):
  
        self.count = count

    def decrement (self):
        self.count = self.count - 1

    def increment (self):
        self.count = self.count + 1

    def is_nil (self):
        if self.data == None:
            return True
        else:
            return False

    def get_left_child (self):
        return self.left_child

    def get_right_child (self):
        return self.right_child

    def get_parent (self):
        return self.parent

    def get_data (self):
        return self.data

    def get_count (self):
        return self.count

    def get_key (self):
        if self.data != None:
            return self.data.get_key()
        else:
            return False

    def compare_key (self, key):
        return self.data.compare_key(key)

    def compare_data (self, object):
        return self.data.compare(object)

    def compare_node (self, node):
        return self.compare_data(node.get_data())

    def child_side (self):

        # Make sure this node isn't the root
        if (self.parent != None):

            # Determine if this node is on the left  or right side
            if(self.parent.get_left_child() == self):
                return Node.LEFT
            else:
                return Node.RIGHT
        
        # This node is the root, return None
        else:
            return None

    def get_sibling (self):

        # Which side is this child node
        side = self.child_side()
        # Return the node opposite this one

        if side == Node.LEFT:
            # print("sibling:", self.parent.get_right_child().get_key())
            return self.parent.get_right_child()

        elif side == Node.RIGHT:
            # print("sibling:", self.parent.get_left_child().get_key())            
            return self.parent.get_left_child()
        
        # This is a root node
        else:
            return None

    def get_uncle (self):
        """
        Returns the uncle node of the current node
        
        Return value:
        A reference to the uncle node
        """

        # Determine if this node is the root or child of the root
        if (self.parent == None) or (self.parent.get_parent() == None):
            return None

        # If not root or child of root, return the parent's sibling (aka the calling node's uncle)
        else:
            return self.parent.get_sibling()            

    def in_order_predecessor (self):

        if (not self.left_child.is_nil()) and (not self.left_child.is_nil()):
            return self.left_child.right_most_node()

    def in_order_successor (self):

        if (not self.is_nil()) and (not self.right_child.is_nil()):
            return self.right_child.left_most_node()

    def right_most_node (self):

        node = self
        finished = False

        while not finished:

            if node.get_right_child().is_nil():
                finished = True
            else:
                node = node.get_right_child()

        return node

    def left_most_node (self):

        node = self
        finished = False

        while not finished:

            if node.get_left_child().is_nil():
                finished = True
            else:
                node = node.get_left_child()

        return node

class BinarySearchTree:
    def __init__ (self):
        self.root = None

    def insert (self, data):
        """
        Insert data into the tree
        """

        return self.insert_node(Node(data, None))

    def insert_node (self, node):
        """
        Insert a node into the tree
        """

        # If tree is empty, let the node be the root
        if self.root == None:
            self.root = node

        else:

            finished = False
            current_node = self.root

            while not finished:

                # The node's key is less than the current node's key
                if node.compare_node(current_node) == -1:
                    if current_node.get_left_child().is_nil():
                        current_node.set_left_child(node)
                        node.set_parent(current_node)
                        finished = True
                    else:
                        current_node = current_node.get_left_child()

                # The node's key is more than the current node's key
                elif node.compare_node(current_node) == 1:
                    if current_node.get_right_child().is_nil():
                        current_node.set_right_child(node)
                        node.set_parent(current_node)
                        finished = True
                    else:
                        current_node = current_node.get_right_child()

                # The node's key is the same as the current node's key
                else:
                    current_node.increment()
                    finished = True

        return node

    def search_node (self, key):
        """
        Search for a node containing the key value
        """

        finished = False
        found = False
        current_node = self.root

        while not finished:

            # Reached NIL node
            if current_node.is_nil():
                finished = True

            elif current_node.compare_key(key) == 1:
                current_node = current_node.get_left_child()

            elif current_node.compare_key(key) == -1:
                current_node= current_node.get_right_child()

            # Key found
            else:
                finished = True
                found = True

        if not found:
            return None
        else:
            return current_node

    def delete(self, key):
        """
        Delete the node containing the key value
        """

        node = self.search_node(key)

        if node == None:
            return None
        elif node.get_count() > 1:
            node.decrement()
            return node.get_count()
        else:
            self.delete_node(node)

    def delete_node (self, node):
        """
        Remove the node from the tree
        """

        # Node has zero children
        if (node.get_left_child().is_nil()) and (node.get_right_child().is_nil()):

            parent_node = node.get_parent()

            if parent_node == None:
                self.root = None
            else:

                # Set parent node's appropriate child to a NIL node
                if (node.child_side() == Node.LEFT):
                    parent_node.set_left_child(Node(None, parent_node))
                else:
                    parent_node.set_right_child(Node(None, parent_node))

        # Node has two children
        elif (not node.get_left_child().is_nil()) and (not node.get_right_child().is_nil()):

            # Set variables for parent and children nodes of current node
            parent_node = node.get_parent()
            node_left_child = node.get_left_child()
            node_right_child = node.get_right_child()

            # Get in-order predecessor node and make a deep copy
            inorder_predecessor = node.in_order_predecessor()
            new_node = inorder_predecessor.copy()

            # Set the new node's parent and child nodes.
            new_node.set_parent(parent_node)
            new_node.set_left_child(node_left_child)
            new_node.set_right_child(node_right_child)

            # Set the parent node's child node to new node
            if parent_node == None:
                self.root = new_node

            else:
                if (node.child_side() == Node.LEFT):
                    parent_node.set_left_child(new_node)
                else:
                    parent_node.set_right_child(new_node)

            # Set child nodes' parent to new node
            node_left_child.set_parent(new_node)
            node_right_child.set_parent(new_node)

            self.delete_node(inorder_predecessor)

        # Node with one children
        else:

            parent_node = node.get_parent()

            # Determine which side the single child node is on
            if not node.get_left_child().is_nil():
                child_node = node.get_left_child()
            else:
                child_node = node.get_right_child()

            # Set the child's parent to the current node's parent
            child_node.set_parent(parent_node)

            if parent_node == None:
                self.root = child_node

            # Determine which side the current node is located, in regards to the parent
            # Set the parent's appropriate child node to the child's child node
            else:
                if node.child_side() == Node.LEFT:
                    parent_node.set_left_child(child_node)
                else:
                    parent_node.set_right_child(child_node)

        return 0

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
                    new_line_string = new_line_string + current_key_string + "{P = " + current_parent_key + "}(" + current_count + ")" + ":"
                else:
                    new_line_string = new_line_string + ", " + current_key_string + "{P = " + current_parent_key + "}(" + current_count + ")" + ":"
            
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