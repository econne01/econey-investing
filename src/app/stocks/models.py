import datetime

from flask import g

class StockHandler(object):

    # Settings for calculating a recent price trend,
    # serves as basic check for a "reasonable" trend period
    # date change in DAYS, price change in PERCENTAGE
    local_extrema_min_date_change = 30
    local_extrema_max_date_change = 365*2
    local_extrema_min_price_change_pct = 0.20

    def get_latest_min_and_max_price_range(self, price_history):
        ''' Return the most recent price extremes (min, max) along
            with dates those prices occurred
            @param Dictionary price_history ie { '2014-01-01': 19.24, '2014-01-31':31.00 }
            @return Tuple (min_price_obj, max_price_obj)
                ie. ({'date':'2014-01-01', 'price':19.24}, {'date':'2014-01-31', 'price':31.00})
        '''
        data = {
            'min_price_date': None,
            'min_price': None,
            'max_price_date': None,
            'max_price': None
        }

        dates = price_history.keys()
        dates.sort()
        dates.reverse()
        for date in dates:
            if data['min_price'] is None or price_history[date] < data['min_price']:
                data['min_price_date'] = date
                data['min_price'] = price_history[date]
            if data['max_price'] is None or price_history[date] > data['max_price']:
                data['max_price_date'] = date
                data['max_price'] = price_history[date]

            min_date = datetime.date(*[int(date_param) for date_param in data['min_price_date'].split('-')])
            max_date = datetime.date(*[int(date_param) for date_param in data['max_price_date'].split('-')])

            price_change_pct = (data['max_price']-data['min_price'])/((data['max_price']+data['min_price'])/2)
            if price_change_pct < self.local_extrema_min_price_change_pct:
                continue
            if abs((max_date-min_date).days) < self.local_extrema_min_date_change:
                continue
            elif abs((max_date-min_date).days) >= self.local_extrema_max_date_change:
                break

            # Once you continue backward in time to a 2nd price change over min threshold,
            # then you have found the 1st complete trend phase
            if data['min_price_date'] < data['max_price_date']:
                earlier_price = data['min_price']
            else:
                earlier_price = data['max_price']

            price_change_pct = (price_history[date]-earlier_price)/((price_history[date]+earlier_price)/2)
            if price_change_pct > self.local_extrema_min_price_change_pct:
                break

        return data

    def get_latest_price_trends(self, tickers):
        ''' Return a list of recent trend data (dates + prices)
            for each ticker in given list
        '''
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

        trends = []
        for ticker in history:
            data = self.get_latest_min_and_max_price_range(history[ticker])
            data['ticker'] = ticker
            trends.append(data)
        return trends
