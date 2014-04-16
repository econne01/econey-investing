econey-investing
==============

Create a local database to store historical stock quote data, pulled from yahoo finance API

Running
-------
To setup:
1. Create the sqlite3 database file 'stocks.db'
2. Make sure the src/stock db/settings.py file points to 'stocks.db'
3. Run setup ``` sqlite3 stocks.db < src/stock_db/schema.sql ```

Macro Economic Indicators (planned)
--------------
http://www.calculatedriskblog.com/2011/06/updated-list-ranking-economic-data.html
- Jobs Report
- Consumer Sentiment
- Inflation (CPI)
- ICEE Put/Call ratio
- Investor Intelligence Bull/Bear ratio
- Population Demographics
- Home Sales / Starts
- Auto sales
- GDP
- Retail Sales
- ISM Manufacturing Index
- BEA Personal Income and Outlays
- AAR Rail traffic
- Consumer confidence
- M2 Money Supply
- Mutual Fund flows
- Durable Goods report
- Fed reports (New York, Philly, Kansas City...)
- Beige Book
