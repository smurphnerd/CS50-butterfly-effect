from flask import session, flash
from cs50 import SQL

# Add database
db = SQL('sqlite:///butterfly-effect.db')


# Make a new root
def add_root(message):
    # Check message is valid
    if len(message) < 1:
        return flash('invalid message')
    
    # Get key
    existing_roots = db.execute('SELECT roots FROM users WHERE id = ?', session['user_id'])[0]['roots']
    new_roots = existing_roots + 1
    key = 'r' + str(new_roots)

    # Add root count into users
    db.execute('UPDATE users SET roots = ? WHERE id = ?', new_roots, session['user_id'])

    # Add root to database
    db.execute('INSERT INTO nodes (user_id, key, message) VALUES (?, ?, ?)', session['user_id'], key, message)

    return


# Make a new node
def add_child(node_id, message):
    parent = db.execute('SELECT * FROM nodes WHERE id = ?', node_id)

    # Ensure a valid message
    if len(message) < 1:
        return flash('invalid message')

    # Check that parent key exists
    elif len(parent) != 1:
        return flash('no parent')
    
    else:
        # Get key for child
        parent_key = parent[0]['key']
        child_key = parent_key + '.' + str(db.execute('SELECT COUNT(parent_key) FROM children WHERE node_id = ?',
                                                 node_id)[0]['COUNT(parent_key)'] + 1)
        

        # Insert node
        db.execute('INSERT INTO nodes (user_id, key, message) VALUES (?, ?, ?)', session['user_id'], child_key, message)

        # Insert as child
        db.execute('INSERT INTO children (user_id, node_id, parent_key, child_key) VALUES (?, ?, ?, ?)', session['user_id'], node_id, parent_key, child_key)

        return


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
    siblings = db.execute('SELECT child_key FROM children WHERE user_id = ? AND parent_key = ? AND child_key > ?', session['user_id'], key[:-2], key)

    # Rename all siblings and their children
    for sibling in siblings:
        old_key = sibling['child_key']

        # Get new key (eg. 1.2 -> 1.1)
        new_key = old_key[:-1] + str((int(old_key[-1]) - 1))

        # Update values in nodes and children tables
        db.execute('UPDATE children SET parent_key = REPLACE(parent_key, ?, ?), child_key = REPLACE(child_key, ?, ?) WHERE user_id = ?',
                   old_key, new_key, old_key, new_key, session['user_id'])
        db.execute('UPDATE nodes SET key = REPLACE(key, ?, ?) WHERE user_id = ?', old_key, new_key, session['user_id'])


def get_json(root_key):
    # Find the root node
    root = db.execute('SELECT * FROM nodes WHERE user = ? AND key = ?', session['user_id'], root_key)[0]
    generate_tree(root)


def generate_tree(root):
    children = db.execute('SELECT * FROM children WHERE node_id = ?', root['id'])
    if len(children) != 0:
        
    # Get the message
    