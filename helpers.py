from functools import wraps
from flask import g, request, redirect, url_for

"""https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/"""

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function