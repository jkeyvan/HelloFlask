import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash,make_response
from contextlib import closing

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
#app.config.from_envvar('CONFIC', silent=True)
app.config.from_object(__name__)



def valid_login(username,password):
    if username=='j,keyvan' and password=="123456":
        return True


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def log_the_user_in():
    pass

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
        [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]


    if 'usetname' in session:
        status='your are login'
    else:status='your are not login , please sign in '

    return render_template('show_entries.html', entries=entries,status=status)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
<form action="" method="post">
<p><input type=text name=username>
<p><input type=submit value=Login>
</form>
'''
@app.route('/logout')
def logout():
# remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
# set the secret key. keep this really secret:

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/post/<int:post_id>')
def show_post(post_id):
# show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/login',methods=['POST','GET'])
def login(name):
    error=None
    if request.method=='POST':
        if valid_login(request.form('username'),
                       request.form('password')):
            log_the_user_in()
    else:
        error="invalid usename or password"
    return render_template('login.html',error=error)



@app.route('/user/<username>')
def profile(username): pass

@app.route('/lo')
def func():
    resp = make_response(render_template('home.html'))
    resp.set_cookie('username', 'the username')
    return resp
if __name__ == '__main__':
    app.debug=True
    app.run()


