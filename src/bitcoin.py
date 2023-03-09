from prometheus_client import Histogram, start_http_server
import requests
import json
import time
from datetime import datetime, timedelta
import sys


def bitcoin_value():
    # Définir un histogramme Prometheus pour suivre les valeurs quotidiennes du bitcoin
    bitcoin_values = Histogram('bitcoin_values', 'Valeur quotidienne du bitcoin en USD', buckets=[i*1000 for i in range(10, 100)])

    # Démarrer le serveur HTTP de Prometheus
    start_http_server(8000)

    # Boucle pour envoyer des données à Prometheus
    date = "2021-10-10"
    while date < time.strftime("%Y-%m-%d"):
        # Récupérer la valeur du bitcoin pour la date actuelle
        response = requests.get(f"https://api.coindesk.com/v1/bpi/historical/close.json?start={date}&end={date}")
        data = json.loads(response.text)
        value = data['bpi'][date]
        print(value)
        # Ajouter la valeur à l'histogramme
        bitcoin_values.observe(float(value))
        # Passer à la date suivante
        date = datetime.strptime(date, '%Y-%m-%d')
        date = date + timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        print(date)
        # date = time.strftime("%Y-%m-%d", time.gmtime(time.mktime(time.strptime(date, "%Y-%m-%d")) + 86400))
    print(bitcoin_values)
    return bitcoin_values


def main():
    bitcoin_value()

if __name__ == '__main__':
    sys.exit(main())