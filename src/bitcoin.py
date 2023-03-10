from prometheus_client import Histogram, start_http_server
import requests
import json
import time
from datetime import datetime, timedelta
import sys
import os

data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/bitcoin_values.json"

def bitcoin_value():
    # Définir un histogramme Prometheus pour suivre les valeurs quotidiennes du bitcoin
    bitcoin_values = Histogram('bitcoin_values', 'Valeur quotidienne du bitcoin en USD', buckets=[i*1000 for i in range(10, 100)])
    
    taille = os.stat(data_file).st_size

    if (taille != 0):
        with open(data_file, 'r') as f:
            bitcoin_data = json.loads(f.read())
        print(bitcoin_data)
        old_dates = list(bitcoin_data.keys())
        print(old_dates)
        last_date = old_dates[len(old_dates)-1]
        print(last_date)
    else : 
        last_date = "2021-10-10"
        bitcoin_data = {}

    while last_date < time.strftime("%Y-%m-%d"):
        # Récupérer la valeur du bitcoin pour la date actuelle
        response = requests.get(f"https://api.coindesk.com/v1/bpi/historical/close.json?start={last_date}&end={last_date}")
        data = json.loads(response.text)
        print(data)
        try:
            value = data['bpi'][last_date]
        except:
            last_key = list(bitcoin_data.keys())[-1]
            print(last_key)
            value = bitcoin_data[last_key]
            
        print(value)
        bitcoin_data[last_date] = value
        # Ajouter la valeur à l'histogramme
        bitcoin_values.observe(float(value))
        # Passer à la date suivante
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        last_date = last_date + timedelta(days=1)
        last_date = last_date.strftime('%Y-%m-%d')
        print(last_date)
        
        # date = time.strftime("%Y-%m-%d", time.gmtime(time.mktime(time.strptime(date, "%Y-%m-%d")) + 86400))
    with open(data_file, 'w') as f:
        json.dump(bitcoin_data, f, indent=4, sort_keys=True)

    print(bitcoin_data)
    return bitcoin_values

def graph_bitcoin(bitcoin_values):
    return 0


def main():
    bitcoin_value()

    # Démarrer le serveur HTTP de Prometheus
    start_http_server(8000)

if __name__ == '__main__':
    sys.exit(main())