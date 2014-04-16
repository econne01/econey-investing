import sqlite3

class StockProfileView(object):

    def view_response(self, ticker):
        date, price = '?', '?'

        conn = sqlite3.connect('stocks.db')
        c = conn.cursor()

        c.execute('''
            SELECT date, price FROM stocks
            WHERE ticker=?
            ORDER BY date DESC
            ''',
            (ticker,)
        )
        last_row = c.fetchone()
        if last_row is not None:
            date = last_row[0]
            price = last_row[1]

        conn.close()
        return 'Date: %s, Price: %s' %(date, price)