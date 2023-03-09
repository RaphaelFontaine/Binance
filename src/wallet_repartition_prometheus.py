import sys
import matplotlib.pyplot as plt
import numpy as np
from get_wallet import *
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge
from wallet_value import *
from get_operations import *
from get_actual_wallet_value import get_portfolio_value

def actual_portfolio_value():
    value = get_portfolio_value()
    actual_value = Gauge('Actual value', 'Actual value of my wallet')
    actual_value.send(value)
    return 0

def wallet_deposit_data():
    total_deposit = get_deposit_history("0")
    deposit = Gauge('Deposit', 'Total deposit')
    deposit.set(total_deposit)
    return 0

def wallet_withdrawal_data():
    total_withdraw = get_deposit_history("1")
    woithdraw = Gauge('Withdrawal', 'Total withdrawal')
    woithdraw.set(total_withdraw)
    return 0


def wallet_value_data():

    gauge_metric = Gauge('wallet_value', 'Wallet value depending on the date', ['date'])

    L = wallet_value()
    dates = L[0]
    wallet_values = L[1]

    for k in range(len(dates)):
        date  = dates[k]
        unix_date = int(datetime.datetime.timestamp(date))
        # print(type(date))
        value = wallet_values[k]
        # timestamp = int(date.timestamp())
        gauge_metric.labels(date=date).set(value)

    return 0

def wallet_repartition_data():

    wallet = get_wallet_capitalization_by_crypto()

    crypto_names = list(wallet.keys())
    crypto_values = list(wallet.values())

    for k in range(len(crypto_names)):
        name = crypto_names[k] + 'value'
        value_name =  crypto_names[k]
        value_legend = 'Valeur en Euro du ' + crypto_names[k]
        name = Gauge(value_name, value_legend)
        name.set(crypto_values[k])

    return 0
    

def main():

    actual_portfolio_value()
    wallet_deposit_data()
    wallet_withdrawal_data()
    
    wallet_value_data()
    wallet_repartition_data()

    start_http_server(8000)
    
    while True:
        pass


if __name__ == '__main__':
    sys.exit(main())
    