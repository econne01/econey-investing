import sqlite3
from stockretriever import stockretriever
from stock_history.tickers import Tickers

from stock_db import settings

if __name__ == '__main__':
    conn = sqlite3.connect(settings.DATABASE)
    c = conn.cursor()

    sr = stockretriever.StockRetriever()

    for industry in Tickers.tickers:
        for tkr in Tickers.tickers[industry]:
            print 'Getting prices for %s' %(tkr)
            info = sr.get_historical_info(tkr)
            for row in info[:5]:
                c.execute('''
                    UPDATE stocks
                    SET volume=?, price=?
                    WHERE date=? and ticker=?''',
                    (row['Volume'], row['AdjClose'], row['Date'], tkr,)
                )
                if c.rowcount == 0:
                    c.execute('''
                        INSERT into stocks (date, ticker, volume, price)
                        values (?,?,?,?)''',
                        (row['Date'], tkr, row['Volume'], row['AdjClose'],)
                    )

    conn.commit()
    conn.close()

