import sys
import matplotlib.pyplot as plt
import numpy as np
from get_wallet import *
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge
from wallet_value import *
from get_operations import *
from get_actual_wallet_value import get_portfolio_value
import json

def actual_portfolio_value():
    value = get_portfolio_value()
    actual_value = Gauge('Actual_value', 'Actual value of my wallet')
    actual_value.set(value)
    return 0

def wallet_operations_data():

    data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/operations.json"

    with open(data_file, 'r') as f:
        data = json.load(f)
    
    gauge_deposits = Gauge('deposits', 'All deposits completed', ['date'])

    # Parcourir les données de dépôt et mettre à jour le métrique Gauge
    for date, amount in data['deposits'].items():
        gauge_deposits.labels(date=date).set(amount)

    gauge_withdrawals= Gauge('withdrawal', 'All withdrawal completed', ['date'])

    # Parcourir les données de dépôt et mettre à jour le métrique Gauge
    for date, amount in data['withdrawal'].items():
        gauge_withdrawals.labels(date=date).set(amount)



def wallet_value_data():

    gauge_wallet_value = Gauge('wallet_value', 'Wallet value depending on the date', ['date', 'trigram'])
    data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/wallet_value.json"
    with open(data_file, 'r') as f:
        wallet_value_data = json.loads(f.read())
    
    dates = list(wallet_value_data.keys())
    
    for k in range(len(dates)):
        date  = dates[k]
        cryptos = list(wallet_value_data[date].keys())
        for i in range(len(cryptos)):
            trigram = cryptos[i]
            value = wallet_value_data[date][trigram]
            gauge_wallet_value.labels(date=date, trigram=trigram).set(value)
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

def bitcoin_values_data():

    data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/bitcoin_values.json"

    with open(data_file, 'r') as f:
        wallet_value_data = json.loads(f.read())

    gauge_bitcoin = Gauge('bitcoin', 'Bitcoin value', ['date'])

    for date, value in wallet_value_data.items():
        gauge_bitcoin.labels(date).set(value)

    return 0

    

def main():

    try:
        actual_portfolio_value()
    except:
        print("Error when sending actual wallet value")

    #Error
    try:
        wallet_operations_data()
    except:
        print("Error when sending operations")

    #Error
    try:
        wallet_value_data()
    except:
        print("Error when sending wallet value data")

    try:
        wallet_repartition_data()
    except:
        print("Error when sending wallet repartition data")

    try:
        bitcoin_values_data()
    except:
        print("Error when sending bitcoin data")


    start_http_server(8000)

    while True:
        pass


if __name__ == '__main__':
    sys.exit(main())
    