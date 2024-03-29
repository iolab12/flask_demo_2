# imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = 'polls.db'
DEBUG = True
SECRET_KEY = 'development key'

# create application
app = Flask(__name__)
app.config.from_object(__name__)

# initialize database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


# home page
@app.route("/")
def home():
    return render_template('home.html')


# register users
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if(request.form['username'] == "" or request.form['password'] == "" or request.form['firstname']  == "" or request.form['lastname'] == ""):
            error = "invalid form"
            return render_template('register.html', error=error)

        # TODO
        # Check if a username already exists in the database and return an error


        g.db.execute('insert into users (username, password, firstname, lastname) values (?, ?, ?, ?)',
                            [request.form['username'], request.form['password'], request.form['firstname'], request.form['lastname']])
        g.db.commit()
        flash('successfully registered!')
        session['logged_in'] = True
        session['username'] = request.form['username']
        return redirect(url_for('show_polls'))

    return render_template('register.html', error=error)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users where username = ? and password = ?', [request.form['username'], request.form['password']])
        if not cur.fetchall():
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_polls'))
        return render_template('login.html', error=error)

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route("/about/")
def about():
    return "This is an about page"

@app.route("/show_polls/", methods=['GET', 'POST'])
def show_polls():
    error = None
    if session['logged_in'] == False:
        redirect(url_for('home'))

    username = session.get('username')
    # POST REQUESTS ARE FOR ADDING
    if request.method == 'POST':
        # if the user is logged in, add the new poll
        # dont forget to check for an empty string
        # TODO
        
        return render_template('polls.html',username=username, error=error)
        
    return render_template('polls.html',username=username, error=error)

if __name__ == "__main__":
    app.run();
