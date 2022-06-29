import json
from cs50 import SQL

db = SQL('sqlite:///butterfly-effect.db')

# root_object = {}
# root_data = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', )[0]
# root_object['id'] = root_data['id']
# root_object['message'] = root_data['message']
# add_children(root_object)

# def add_children(root_object):
#     children = db.execute('SELECT * FROM children WHERE node_id = ?', )
#     if len(children) > 0:
#         root_object['children'] = []
#         for child in children:
#             child_object = {}
#             child_data = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', )[0]
#             child_object['id'] = child_data['id']
#             child_object['message'] = child_data['message']
#             add_children(child_object)
#             root_object['children'].append(child_object)
#             return
#     else:
#         return

"""
define root attributes

Add children (root)
    If root has children
        root[children] = []
        For each child, add attributes
        Add children (child)
        Append child to root children
    else
        return
"""

# Recursively delete a node's children
def delete_node(node_id):
    children = db.execute('SELECT child_id FROM children WHERE parent_id = ?', node_id)

    # Base case - delete this node from nodes and children tables
    if len(children) == 0:
        db.execute('DELETE FROM children WHERE child_id = ?', node_id)
        db.execute('DELETE FROM nodes WHERE id = ?', node_id)
        return
    
    # Delete each child from the children list
    for child in children:
        delete_node(db.execute('SELECT id FROM nodes WHERE id = ?', child['child_id'])[0]['id'])
    
    # Delete the root node
    db.execute('DELETE FROM children WHERE child_id = ?', node_id)
    db.execute('DELETE FROM nodes WHERE id = ?', node_id)

    return


# Delete a node and recursively delete subsequent children
def delete_node(node_id):
    children = db.execute('SELECT child_id FROM children WHERE parent_id = ?', node_id)

    # Base case - delete this node from nodes and children tables
    if len(children) == 0:
        db.execute('DELETE FROM children WHERE child_id = ?', node_id)
        db.execute('DELETE FROM nodes WHERE id = ?', node_id)
        return
    
    # Delete each child from the children list
    for child in children:
        delete_node(db.execute('SELECT id FROM nodes WHERE id = ?', child['child_id'])[0]['id'])
    
    db.execute('DELETE FROM children WHERE child_id = ?', node_id)
    db.execute('DELETE FROM nodes WHERE id = ?', node_id)
    
    return

delete_node(19)