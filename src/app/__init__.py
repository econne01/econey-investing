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

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(Settings.SYNCDB_SQL, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), single_row=False):
    cur = get_db().execute(query, args)

    if query.strip()[:6].upper() in ['INSERT', 'UPDATE']:
        g._database.commit()

    results = cur.fetchall()
    cur.close()
    if single_row:
        return results[0]
    else:
        return results


def main():
    app.run()

