from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

from helpers import login_required
import bfly

# Configure application
app = Flask(__name__)
app.secret_key = 'dev'
app.permanent_session_lifetime = timedelta(days=365)

# Configure CS50 Library to use SQLite database
db = SQL('sqlite:///butterfly-effect.db')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Default home page"""

    # Reached via POST
    if request.method == 'POST':
        
        # Add a root node
        if 'add-root' in request.form:
            message = request.form['message']

            bfly.add_root(message)

            return redirect('/')

        # Add a child node
        if 'add-child' in request.form:
            node_id = request.form['node-id']
            message = request.form['message']

            bfly.add_child(node_id, message)

            return redirect('/')

        # Edit a node's message
        if 'edit-message' in request.form:
            node_id = request.form['node-id']
            message = request.form['message']

            db.execute('UPDATE nodes SET message = ? WHERE id = ?', message, node_id)

            return redirect('/')

        # Delete a node and its children
        if 'delete-node' in request.form:
            node_id = int(request.form['node-id'])

            node = db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', session['user_id'], node_id)

            if len(node) != 1:
                flash('invalid id')

            else:
                bfly.delete_node(node_id)

                # Check if the deleted node was the session node
                if node_id == session['root_id']:
                        roots = db.execute('SELECT id FROM nodes WHERE user_id = ? AND root_node = 1', session['user_id'])
                        # Change the default root to the latest root
                        if len(roots) >= 1:
                            session['root_id'] = roots[-1]['id']
                        
                        # Clear the default root
                        else:
                            session.pop('root_id', default=None)

            return redirect('/')

        # Change the session's default root
        if 'root-session' in request.form:

            if len(db.execute('SELECT * FROM nodes WHERE user_id = ? AND id = ?', session['user_id'], request.form['node-id'])) != 1:
                flash('invalid id')
            
            else:
                session['root_id'] = int(request.form['node-id'])

            return redirect('/')
    
    # Reached via GET
    if 'root_id' in session:
        bfly.init_json(session['root_id'])
    
    else:
        bfly.init_json(None)

    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register an account"""

    # Reached via POST
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        # Invalid usernames
        if not user:
            flash('must provide username')
        elif db.execute('SELECT * FROM users WHERE username = ?', user):
            flash('username already taken')
        
        # Invalid passwords
        elif len(password) < 9:
            flash('password must be at least 8 characters')
        elif password != request.form['confirm']:
            flash('passwords don\'t match')

        # If all checks are passed, add to database
        else:
            hash = generate_password_hash(password)
            db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', user, hash)

            # Go to login screen
            return redirect('/login')
        
        return redirect('/register')
    
    # Reached via GET


    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Clear session
    session.pop('user_id', default=None)
    session.pop('root_id', default=None)

    # Reached via POST
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        rows = db.execute('SELECT * FROM users WHERE username = ?', user)

        # Ensure there is a username and password
        if not user:
            flash('must enter a username', 'error')
        elif not password:
            flash('must enter a password', 'error')

        # Ensure username exists and password is correct
        elif len(rows) != 1 or not check_password_hash(rows[0]['password_hash'], password):
            flash('username or password is incorrect', 'error')
            
        # If valid, create a permanent session
        else:
            session.permanent = True
            session['user_id'] = rows[0]['id']

            # Access to index page
            return redirect('/')
        
        return redirect('/login')
    
    # Reached via GET
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log user out"""

    session.pop('user_id', default=None)
    session.pop('root_id', default=None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)