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
    actual_value = Gauge('Actual_value', 'Actual value of my wallet')
    actual_value.set(value)
    return 0

def wallet_deposit_data():
    total_deposit = get_deposit_history("0")[0]
    deposit = Gauge('Deposit', 'Total deposit')
    deposit.set(total_deposit)
    return 0

def wallet_historical_deposit_data():
    deposits = get_deposit_history("0")[1]
    aux = "depot"
    for k in range(len(deposits[0])):
        name = aux + str(k+1)
        print(name)
        value_deposit = deposits[1][k]
        value_name =  name + str(k+1)
        value_legend = 'Depot numero ' + str(k+1)
        name = Gauge(deposits[0][k], value_legend)
        name.set(value_deposit)
        aux = "depot"
    return 0

def wallet_withdrawal_data():
    total_withdraw = get_deposit_history("1")[0]
    withdraw = Gauge('Withdrawal', 'Total withdrawal')
    withdraw.set(total_withdraw)
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

    try:
        actual_portfolio_value()
    except:
        print("Error when getting actual wallet value")

    try:
        wallet_historical_deposit_data()
    except:
        print("Error when getting historical deposits")

    try:
        wallet_deposit_data()
    except:
        print("Error when getting total deposit")

    try: 
        wallet_withdrawal_data()
    except:
        print("Error when getting total withdrawal")

    
    wallet_value_data()
    wallet_repartition_data()

    start_http_server(8000)
    
    while True:
        pass


if __name__ == '__main__':
    sys.exit(main())
    