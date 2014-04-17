from flask import g, render_template
from app import app

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

