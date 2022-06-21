from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

from helpers import login_required

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
        pass
    
    # Reached via GET
    return render_template('index.html', user=session['user'])


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register an account"""

    # Reached via POST
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        # Invalid usernames
        if not user:
            return redirect(url_for('register', error='must provide username'))
        if db.execute('SELECT * FROM users WHERE username = ?', user):
            return redirect(url_for('register', error='username already taken'))
        
        # Invalid passwords
        if len(password) < 9:
            return redirect(url_for('register', error='password must be at least 8 characters'))
        if password != request.form['confirm']:
            return redirect(url_for('register', error='passwords don\'t match'))

        # If all checks are passed, add to database
        hash = generate_password_hash(password)
        db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', user, hash)

        # Go to login screen
        return redirect('/login')
    
    # Reached via GET
    if request.method == 'GET':
        error = ''
        if request.args:
            error = request.args['error']
        return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    
    # Clear session
    session.pop('user_id', default=None)

    # Reached via POST
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        # Ensure there is a username and password
        if not user:
            return redirect(url_for('login', error='must enter a username'))
        if not password:
            return redirect(url_for('login', error='must enter a password'))

        # Ensure username exists and password is correct
        rows = db.execute('SELECT * FROM users WHERE username = ?', user)
        if len(rows) != 1 or not check_password_hash(rows[0]['password_hash'], password):
            return redirect(url_for('login', error='username or password is incorrect'))
            
        # If valid, create a permanent session
        session.permanent = True
        session['user_id'] = rows[0]['id']

        return redirect('/')
    
    # Reached via GET
    error = ''
    if request.args:
        error = request.args['error']
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    """Log user out"""

    # Clear session
    session.pop('user_id', default=None)
    return redirect('/login')