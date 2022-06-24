from cs50 import SQL
from flask import flash

db = SQL('sqlite:///butterfly-effect.db')

# Call to all functions related to deleting a node
def delete_node(node_id):
    node = db.execute('SELECT * FROM nodes WHERE id = ?', node_id)

    if len(node) != 1:
        return flash('invalid id')
    
    # Call function to delete children
    delete_children(node_id)

    # Delete the node
    db.execute('Delete FROM children WHERE node_id = ? OR child_key = ?', node_id, node[0]['key'])
    db.execute('DELETE FROM nodes WHERE id = ?', node_id)

    # Rename the node's siblings
    rename_nodes(node[0]['key'])
    return


# Delete a node and recursively delete subsequent children
def delete_children(node_id):
    children = db.execute('SELECT child_key FROM children WHERE node_id = ?', node_id)

    # Base case - delete this node from nodes and children tables
    if len(children) == 0:
        db.execute('Delete FROM children WHERE node_id = ?', node_id)
        db.execute('DELETE FROM nodes WHERE id = ?', node_id)
        return
    
    # Delete each child from the children list
    for child in children:
        node_id = db.execute('SELECT id FROM nodes WHERE key = ? AND user_id = 1', child['child_key'])[0]['id']
        delete_children(node_id)
    
    return


def rename_nodes(key):
    # Get list of siblings that are larger than the key
    siblings = db.execute('SELECT child_key FROM children WHERE user_id = 1 AND parent_key = ? AND child_key > ?', key[:-2], key)

    # Rename all siblings and their children
    for sibling in siblings:
        old_key = sibling['child_key']

        # Get new key (eg. 1.2 -> 1.1)
        new_key = old_key[:-1] + str((int(old_key[-1]) - 1))

        # Update values in nodes and children tables
        db.execute('UPDATE children SET parent_key = REPLACE(parent_key, ?, ?), child_key = REPLACE(child_key, ?, ?) WHERE user_id = 1',
                   old_key, new_key, old_key, new_key)
        db.execute('UPDATE nodes SET key = REPLACE(key, ?, ?) WHERE user_id = 1', old_key, new_key)

rename_nodes('r10.1')