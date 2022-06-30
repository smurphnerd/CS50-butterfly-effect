from flask import session, flash
from cs50 import SQL
import json

# Add database
db = SQL('sqlite:///butterfly-effect.db')


# Make a new root
def add_root(message):
    # Check message is valid
    if len(message) < 1:
        return flash('invalid message')

    # Add root to database
    db.execute('INSERT INTO nodes (user_id, message, root_node) VALUES (?, ?, 1)', session['user_id'], message)

    # Update the session's root
    session['root_id'] = db.execute('SELECT id FROM nodes WHERE user_id = ? AND root_node = 1', session['user_id'])[-1]['id']

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
        # Insert a new node
        db.execute('INSERT INTO nodes (user_id, message) VALUES (?, ?)', session['user_id'], message)

        # Insert as parent-child relationship
        child_id = db.execute('SELECT id FROM nodes WHERE user_id = ? AND message = ?', session['user_id'], message)[-1]['id']
        db.execute('INSERT INTO children (parent_id, child_id) VALUES (?, ?)', node_id, child_id)

        return


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


# Convert a root to a json file
def init_json(node_id):
    # Get file name
    file = 'user' + str(session['user_id']) + '.json'

    if node_id == None:
        open(file, 'w').close()
        return

    else:
        # Check for valid id
        root = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', session['user_id'], node_id)
        if len(root) != 1:
            return flash('invalid id 1')
        
        # Create a dictionary for the root
        else:
            root_dict = {}
            root_data = root[0]
            root_dict['id'] = root_data['id']
            root_dict['message'] = root_data['message']

            # Call to function to add children to dictionary
            add_children(root_dict, node_id)
            
            # Write the root
            json_object = json.dumps(root_dict, indent = 2)
            with open(file, 'w') as f:
                f.write(json_object)
            
            return


# Recursively add children to the dictionary
def add_children(root_dict, node_id):
    # Check if root node has any children
    children = db.execute('SELECT * FROM children WHERE parent_id = ?', node_id)

    # Add a children's list to the root dictionary
    if len(children) > 0:
        root_dict['children'] = []
        
        # Create a new dictionary for each child
        for child in children:
            child_dict = {}
            child_data = db.execute('SELECT * FROM nodes WHERE id = ?', child['child_id'])[0]
            child_dict['id'] = child_data['id']
            child_dict['message'] = child_data['message']

            # Add the child's children if necessary
            add_children(child_dict, child['child_id'])

            # Add the child object to the root's children list
            root_dict['children'].append(child_dict)
    return