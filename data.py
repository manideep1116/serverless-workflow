
from yahoo_fin.stock_info import *


tickers = ["BTC-USD","ETH-USD","ADA-USD", "DOGE-USD","VET-USD","AAL","AMC"]

def prices(tickers):
    fav_stocks = {}
    for symbol in tickers:
        price = get_live_price(symbol)
        fav_stocks[symbol] = round(price,2)
    return(fav_stocks)



print(prices(tickers))

