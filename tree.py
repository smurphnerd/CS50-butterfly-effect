root_count = 0

class Node:
    """Node for actions to be stored in"""

    def __init__(self, key: str, message: str, parent = None):

        self.key = key
        self.message = message
        self.children = []
        self.parent = parent


    # Make a child for this node
    def make_child(self, message: str):
        self.children.append(Node(self.get_key(), message, self))
        return


    # Get this node's key
    def get_key(self) -> str:
        key = self.key + '.' + str(len(self.children) + 1)
        return key


    # Return a node from its key
    def find_node_by_key(self, key: str):
        key_list = [int(number) for number in key.split('.')]
        del key_list[0]
        return self.find_node_by_key_list(key_list)


    # Recursive function to find node from key
    def find_node_by_key_list(self, key_list: list):
        if len(key_list) == 0:
            return self
    
        latest_key = key_list.pop(0)
        self = self.children[latest_key - 1]
        return self.find_node_by_key_list(key_list)


    # Delete's a node and its children
    def delete_node(self):
    
        # Find position in parent's array
        position = [int(number) for number in self.key.split('.')][-1] - 1
        del self.parent.children[position]
        return
    
    # Edit a node's message
    def edit_message(self, message: str):
        self.message = message


def create_root(message: str) -> Node:
    global root_count
    root_count += 1
    key = str(root_count)
    root = Node(key, message)
    return root


# Prints the n-ary tree level wise (to delete later)
def LevelOrderTraversal(root: Node):
    """https://www.geeksforgeeks.org/generic-tree-level-order-traversal/"""
 
    if (root == None):
        return
   
    # Standard level order traversal code
    # using queue
    q = []  # Create a queue
    q.append(root); # Enqueue root
    while (len(q) != 0):
     
        n = len(q)
  
        # If this node has children
        while (n > 0):
         
            # Dequeue an item from queue and print it
            p = q[0]
            q.pop(0)
            print(f'({p.key}) {p.message}', end=' ')
   
            # Enqueue all children of the dequeued item
            for i in range(len(p.children)):
             
                q.append(p.children[i])
            n -= 1
   
        print() # Print new line between two levels