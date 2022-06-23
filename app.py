from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

from helpers import login_required, apology

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
        
        #if request.form['add-child']
        # Ensure input was provided
        message = request.form['root']
        if len(message) == 0:
            return redirect('/')
        
        # Get key
        existing_roots = db.execute('SELECT roots FROM users WHERE id = ?', session['user_id'])[0]['roots']
        new_roots = existing_roots + 1
        key = str(new_roots)

        # Add root count into users
        db.execute('UPDATE users SET roots = ? WHERE id = ?', new_roots, session['user_id'])

        # Add root to database
        db.execute('INSERT INTO nodes (user_id, key, message) VALUES (?, ?, ?)', session['user_id'], key, message)
        return redirect('/')
    
    # Reached via GET
    if db.execute('SELECT roots FROM users WHERE id = ?', session['user_id'])[0]['roots'] == 0:
        return render_template('index.html')

    return render_template('index.html', root='there is a root')


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
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)