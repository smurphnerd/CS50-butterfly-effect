from flask import session, flash
from cs50 import SQL

# Add database
db = SQL('sqlite:///butterfly-effect.db')


# Make a new root
def add_root(message):
    # Check message is valid
    if len(message) < 1:
        return flash('invalid message')

    # Add root to database
    db.execute('INSERT INTO nodes (user_id, message, root_node) VALUES (?, ?, 1)', session['user_id'], message)

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


# def get_json(root_key):
#     # Find the root node
#     root = db.execute('SELECT * FROM nodes WHERE user = ? AND key = ?', session['user_id'], root_key)[0]
#     generate_tree(root)


# def generate_tree(root):
#     children = db.execute('SELECT * FROM children WHERE node_id = ?', root['id'])
#     if len(children) != 0:
        
#     # Get the message
    