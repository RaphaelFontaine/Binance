from get_wallet import *
import sys

keys = get_keys()
api_key = keys[0]
api_secret = keys[1]

def get_portfolio_value():
    client = Client(api_key, api_secret)
    ticker_prices = client.get_all_tickers()
    
    portfolio = client.get_account()
    portfolio = portfolio["balances"]
    total_value = 0

    for balance in portfolio:
        if float(balance['free']) > 0 or float(balance['locked']) > 0:
            symbol = balance['asset'] + 'EUR'
            ticker_price = next((item for item in ticker_prices if item["symbol"] == symbol), None)
            if ticker_price:
                total_value += float(balance['free']) * float(ticker_price['price'])
    return total_value

def main():
    get_portfolio_value()

if __name__ == '__main__':
    sys.exit(main())