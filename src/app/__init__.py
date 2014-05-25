import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from settings.common import Settings

SETTINGS_MODULE = 'settings.flask'

app = Flask(
    __name__,
    static_folder=Settings.STATIC_DIRECTORY,
    template_folder=Settings.TEMPLATE_DIRECTORY
)
app.config.from_object(SETTINGS_MODULE)
app.config['UPLOAD_FOLDER'] = Settings.UPLOAD_DIRECTORY

from app.stocks import views

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(SETTINGS_MODULE, mode='r') as f:
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

def main():
    app.run()

