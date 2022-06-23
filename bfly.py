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

    # Add root count into users
    db.execute('UPDATE users SET roots = ? WHERE id = ?', new_roots, session['user_id'])

    # Add root to database
    db.execute('INSERT INTO nodes (user_id, key, message) VALUES (?, ?, ?)', session['user_id'], str(new_roots), message)

    return


# Make a new node
def add_child(parent_key, message):
    parent = db.execute('SELECT * FROM nodes WHERE user_id = ? AND key = ?', session['user_id'], parent_key)

    # Ensure a valid message
    if len(message) < 1:
        return flash('invalid message')

    # Check that parent key exists
    elif len(parent) != 1:
        return flash('no parent')
    
    else:
        # Get key for child
        child_key = parent[0]['key'] + '.' + str(db.execute('SELECT COUNT(key) FROM children WHERE user_id = ? AND key = ?', session['user_id'], parent_key)[0]['COUNT(key)'] + 1)

        # Insert node
        db.execute('INSERT INTO nodes (user_id, key, message, parent) VALUES (?, ?, ?, ?)', session['user_id'], child_key, message, parent_key)

        # Insert as child
        db.execute('INSERT INTO children (user_id, key, child_key) VALUES (?, ?, ?)', session['user_id'], parent_key, child_key)

        return


