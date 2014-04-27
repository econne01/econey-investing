from flask import g, render_template
from app import app
from app.stocks.models import Stock

#---- VIEWS ----#
@app.route('/')
def home():
    cur = g.db.execute('''
        SELECT ticker, date, volume, price
        FROM stocks
        GROUP BY ticker
        ORDER BY ticker, date DESC
    ''')
    entries = [row for row in cur.fetchall()]
    return render_template('home2.html', entries=entries)

@app.route('/trends')
def trends():
    cur = g.db.execute('''
        SELECT ticker, date, price, volume
        FROM stocks
        ORDER BY ticker, date DESC
    ''')
    data = cur.fetchall()

    history = {}
    for row in data:
        ticker, date, price, volume = row
        if ticker not in history:
            history[ticker] = {}
        history[ticker][date] = price

    trends = {}
    for ticker in history:
        trends[ticker] = Stock().get_latest_min_and_max_price_range(history[ticker])
    return render_template('trends.html', trends=trends)

