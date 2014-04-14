import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


#from stock_history.views import stock_profile
#
#app = Flask(__name__)
#
#@app.route('/')
#def hello_world():
#    return 'Hello World!'
#
#@app.route('/<ticker>')
#def show_stock_profile(ticker):
#    view = stock_profile.StockProfileView().view_response(ticker)
#    return view
#
#def main():
#    app.debug = True
#    app.run()

# FLASK_SETTINGS = 'stock_db/settings.py'
app = Flask(__name__)
app.config.from_object('stock_db.settings')
app.config.from_envvar('STOCK_DB_SETTINGS', silent=True)

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
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    rs = None

    db = getattr(g, 'db', None)
    if db is not None:
        cur = db.execute(query, args)
        rs = cur.fetchall()
        cur.close()
    return (rs[0] if rs else None) if one else rs

#---- VIEWS ----#
@app.route('/')
def home():
    cur = g.db.execute('''
        SELECT ticker, date, volume, price
        FROM stocks
        ORDER BY ticker, date DESC
    ''')
    entries = [row for row in cur.fetchall()]
    return render_template('home.html', entries=entries)


def main():
    app.run()
