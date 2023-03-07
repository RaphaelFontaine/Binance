import sys
import matplotlib.pyplot as plt
import numpy as np
from get_wallet import *
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge

def send_data():

    wallet = get_wallet_capitalization_by_crypto()

    crypto_names = list(wallet.keys())
    crypto_values = list(wallet.values())

    for k in range(len(crypto_names)):
        name = crypto_names[k] + 'value'
        value_name =  crypto_names[k] + '_value_eur'
        value_legend = 'Valeur en Euro du ' + crypto_names[k]
        name = Gauge(value_name, value_legend)
        
        name.set(crypto_values[k])

    start_http_server(8000)

    while True:
        pass
    

def main():
    send_data()


if __name__ == '__main__':
    sys.exit(main())
    
