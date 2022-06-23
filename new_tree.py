from flask import session
from cs50 import SQL
from helpers import apology

# Add database
db = SQL('sqlite:///butterfly-effect.db')


# Make a new node
def add_child(parent_key, message):
    
    # Ensure a valid message
    if len(message) > 1:
        return apology('invalid message', 400)

    # Check that parent key exists
    parent = db.execute('SELECT * FROM nodes WHERE user_id = ? AND key = ?', session['user_id'], parent_key)
    if len(parent) != 1:
        return apology('no key', 400)
    
    # Get key for child
    child_key = parent[0]['key'] + '.' + str(db.execute('SELECT COUNT(key) FROM children WHERE user_id = ? AND key = ?', session['user_id'], parent_key)[0]['COUNT(key)'] + 1)

    # Insert node
    db.execute('INSERT INTO nodes (user_id, key, message, parent) VALUES (?, ?, ?, ?)', session['user_id'], child_key, message, parent_key)

    # Insert as child
    db.execute('INSERT INTO children (user_id, key, child_key) VALUES (?, ?, ?)', session['user_id'], parent_key, child_key)


