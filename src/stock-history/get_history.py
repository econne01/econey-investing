import sqlite3
from stockretriever import stockretriever

if __name__ == '__main__':
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    
    sr = stockretriever.StockRetriever()
    info = sr.get_historical_info('YHOO')
    
    for row in info[:5]:
        c.execute('''
            UPDATE stocks
            SET volume=?, price=?
            WHERE date=? and symbol=?''',
            (row['Volume'], row['AdjClose'], row['Date'], 'YHOO',)
        )
        if c.rowcount == 0:
            c.execute('''
                INSERT into stocks (date, symbol, volume, price)
                values (?,?,?,?)''',
                (row['Date'], 'YHOO', row['Volume'], row['AdjClose'],)
            )
    
    conn.commit()
    