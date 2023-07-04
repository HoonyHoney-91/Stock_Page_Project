import yfinance as yf

def get_buy_stock_user(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    company_name = stock.info
    if company_name is not None:
        short_name = company_name.get('shortName')
        current_price = round(stock.history(period='1d')['Close'].iloc[-1], 2)
        print(short_name)
        return current_price, short_name
    else:
        return None, None

import yfinance as yf

def get_buy_stock_user2(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    company_name = stock.info
    if company_name:
        short_name_2 = company_name.get('shortName')
        current_price_2 = round(stock.history(period='1d')['Close'].iloc[-1], 2)
        print(f"this is short_name_2 ${short_name_2}")
        return short_name_2, current_price_2
    else:
        return None, None