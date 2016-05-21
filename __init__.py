import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash,make_response
from contextlib import closing
from models import post

DATABASE = 'mydb.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
#app.config.from_envvar('CONFIC', silent=True)
app.config.from_object(__name__)



def valid_login(username,password):
    curUsername=g.db.execute('select username,password from members')
    list_of_usernames_and_passwords=[(str(row[0]),str(row[1])) for row in curUsername.fetchall()]
    if (username,password) in list_of_usernames_and_passwords:
        return True
    else:
        return False



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#init_db()

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
    if request.method == 'POST':pass
        #mypost=post(session['username'],request.form['title'],request.form['text'])
        #g.db.execute('insert into entries (username,title, text,rate) values (%s,%s,%s,%s)'%(mypost.user,mypost.title,mypost.text,mypost.rate))
        #g.db.commit()
    flash('New entry was successfully posted')
    return render_template('addEntry.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    curItems = g.db.execute('select title,text from entries where username=%s' % session['username'])
    Items = [(row[0], row[1]) for row in curItems.fetchall()]
    if request.method=='POST':
        username=session['username']
        #username='p'
        title=request.form['title']

        text=request.form['text']
        #mypost = post(session['username'], request.form['title'], request.form['text'])
        rate='0'
        g.db.execute('insert into entries (username,title,text,rate)VALUES (%s,%s,%s,%s)'%(username,title,text,rate))
        g.db.commit()
        #return redirect(url_for('add_entry'))
        Items=[2]
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')

@app.route('/')
def index():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    curUsername = g.db.execute('select username,password from members')
    entries = [(str(row[0]), str(row[1])) for row in curUsername.fetchall()]
    if 'username' in session:
        status='your are login'
        return redirect(url_for('dashboard'))
    else:status='your are not login , please sign in '
    return render_template('show_entries.html', entries=entries,status=status)


'''
<form action="" method="post">
<p><input type=text name=username>
<p><input type=submit value=Login>
</form>
'''
@app.route('/logout')
def logout():
# remove the username from the session if it's there
    session.pop('username', None)
    session['logged_in']=False
    return redirect(url_for('index'))
# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/post/<int:post_id>')
def show_post(post_id):
# show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/login',methods=['POST','GET'])
def login():
    error=None
    if request.method=='POST':
        if valid_login(str(request.form['username']),str(request.form['pass'])):
            session['username'] = request.form['username']
            session['logged_in']=True
            return redirect(url_for('dashboard'))

    else:
        error="invalid usename or password"
        #return error
        #resp=make_response(render_template('home.html'))
    return render_template('log_in_page.html',error=error,session=session)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        print 'hello'
        username=request.form['username']
        email=request.form['email']
        password=request.form['pass']
        g.db.execute('insert into members (username,email,password) VALUES (%s,%s,%s)'%(username,email,password))
        g.db.commit()
        flash('You sign up successfully :)')
        session['username'] = request.form['username']
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('sign_up_page.html')



@app.route('/user/<username>')
def profile(username): pass

@app.route('/lo')
def func():
    resp = make_response(render_template('home.html'))
    resp.set_cookie('username', 'the username')
    return resp
@app.route('/test')
def test():
    #return True
    return render_template('signup.html')



if __name__ == '__main__':
    app.debug=True
    app.run()


