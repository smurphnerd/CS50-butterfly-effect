from functools import wraps
from flask import redirect, session
from cs50 import SQL


def login_required(f):
    """
    Decorate routes to require login

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Add database
db = SQL('sqlite:///butterfly-effect.db')

# Make a child for this node
def make_child(key, message):
    # Check that key exists
    parent = db.execute('SELECT * FROM nodes WHERE user_id = ? AND key = ?', session['user_id'], key)
    if len(parent) != 1:
        return redirect('/index')
