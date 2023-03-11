from prometheus_client import Histogram, start_http_server
import requests
import json
import time
from datetime import datetime, timedelta
import sys
import os
import matplotlib.pyplot as plt

data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/bitcoin_values.json"
DATE = "2021-10-10"

def bitcoin_value():
    # Définir un histogramme Prometheus pour suivre les valeurs quotidiennes du bitcoin
    bitcoin_values = Histogram('bitcoin_values', 'Valeur quotidienne du bitcoin en USD', buckets=[i*1000 for i in range(10, 100)])
    
    taille = os.stat(data_file).st_size

    if (taille != 0):
        with open(data_file, 'r') as f:
            bitcoin_data = json.loads(f.read())
        old_dates = list(bitcoin_data.keys())
        last_date = old_dates[len(old_dates)-1]
    else : 
        last_date = DATE
        bitcoin_data = {}

    while last_date < time.strftime("%Y-%m-%d"):
        # Récupérer la valeur du bitcoin pour la date actuelle
        response = requests.get(f"https://api.coindesk.com/v1/bpi/historical/close.json?start={last_date}&end={last_date}")
        data = json.loads(response.text)
        try:
            value = data['bpi'][last_date]
        except:
            last_key = list(bitcoin_data.keys())[-1]
            value = bitcoin_data[last_key]
            
        bitcoin_data[last_date] = value
        # Ajouter la valeur à l'histogramme
        bitcoin_values.observe(float(value))
        # Passer à la date suivante
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        last_date = last_date + timedelta(days=1)
        last_date = last_date.strftime('%Y-%m-%d')
        
        # date = time.strftime("%Y-%m-%d", time.gmtime(time.mktime(time.strptime(date, "%Y-%m-%d")) + 86400))
    with open(data_file, 'w') as f:
        json.dump(bitcoin_data, f, indent=4, sort_keys=True)

    return 0

def graph_bitcoin():
    with open(data_file, 'r') as f:
        bitcoin_data = json.loads(f.read())

    dates = list(bitcoin_data.keys())
    values = list(bitcoin_data.values())
    
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    # Création de la figure et du graphe
    fig, ax = plt.subplots()

    # Tracé du graphe
    ax.plot(dates, values)

    # Affichage du graphe
    plt.xlabel("Date")
    plt.ylabel("Bitcoin value")
    plt.title("Variation of bitcoin value since October 2021")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    # plt.show()

    aujourd_hui = datetime.now().strftime('%Y-%m-%d')
    plt.savefig('../data/bitcoin/'+aujourd_hui+'.png')


def main():
    bitcoin_value()
    graph_bitcoin()

    # Démarrer le serveur HTTP de Prometheus
    start_http_server(8000)

if __name__ == '__main__':
    sys.exit(main())