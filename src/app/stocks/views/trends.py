from flask import g, render_template, jsonify, request
from app import app
from app.stocks.models import StockHandler

@app.route('/api/trends')
def get_trends():
    ''' Used as API call to return the trend range (dates + prices)
        for each requested ticker
        @param List tickers
    '''
    tickers = request.args.get('tickers', '', type=str)
    tickers = tickers.split(',')

    trends = StockHandler().get_latest_price_trends(tickers)
    return jsonify(trends=trends)

@app.route('/trends')
def trends():
    tickers = []
    trends = StockHandler().get_latest_price_trends(tickers)
    return render_template('trends.html', trends=trends)

