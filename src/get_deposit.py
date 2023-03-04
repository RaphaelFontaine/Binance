import hashlib
import hmac
import requests
import json
import time
import datetime as dt
from get_wallet import *
import sys

keys = get_keys()
api_key = keys[0]
api_secret = keys[1]

DATE = "2021-09-01"

# public static BinanceClient GetClient() { return new BinanceClient(new BinanceClientOptions { ApiCredentials = new CryptoExchange.Net.Authentication.ApiCredentials(key, secret), AutoTimestamp = true }); }

def check_system_time():
    # Récupération de l'heure actuelle du système
    system_time = dt.datetime.now()

    # Récupération de l'heure selon l'API de Binance
    url = "https://api.binance.com/api/v3/time"
    response = requests.get(url)
    server_time = dt.datetime.fromtimestamp(response.json()['serverTime']/1000)

    # Comparaison des deux heures
    time_diff = (server_time - system_time).total_seconds()
    if time_diff > 0:
        print(f"Le système a un retard de {time_diff} secondes par rapport au serveur de temps de Binance")
    elif time_diff < 0:
        print(f"Le système a une avance de {-time_diff} secondes par rapport au serveur de temps de Binance")
    else:
        print("Le système est synchronisé avec le serveur de temps de Binance")
    
def date_to_ms(date_str):
    d = dt.datetime.strptime(date_str, '%Y-%m-%d')
    return int(d.timestamp() * 1000)

def get_ms_since_date(date_str):
    date = dt.datetime.strptime(date_str, '%Y-%m-%d')
    ms_since_epoch = int(date.timestamp() * 1000)
    ms_since_now = int(dt.datetime.now().timestamp() * 1000) - ms_since_epoch
    return ms_since_now

def get_deposit_history(transaction_type):

    ms = date_to_ms(DATE)

    url = "https://api.binance.com/sapi/v1/fiat/orders"

    timestamp = int(dt.datetime.now().timestamp() * 1000)
    print(transaction_type)
    if (transaction_type == 0):
        params = {'transactionType' : "0", 'timestamp': timestamp, 'beginTime' : ms} 
    else:
        params = {'transactionType' : "1", 'timestamp': timestamp, 'beginTime' : ms} 
    headers = {'X-MBX-APIKEY': api_key}

    # Calcul de la signature de la requête
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # Ajout de la signature aux paramètres de la requête
    params['signature'] = signature

    # Envoi de la requête
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.json()}")
        return

    # Traitement de la réponse
    deposits = response.json()['data']
    
    total_deposit = 0
    for deposit in deposits:
        status = deposit['status']
        if (status == 'Successful'):
            amount = deposit['indicatedAmount']
            total_deposit = total_deposit + float(amount)
    if (transaction_type == 0):
        print(f"TOTAL DEPOSIT : {total_deposit}")
    else:
        print(f"TOTAL WITHDRAWS : {total_deposit}")
    return total_deposit

def main():
    print(len(sys.argv))
    if (len(sys.argv) == 1):
        print("Enter an arg : \n - 0 : deposits \n - 1 withdrawals")
        return 0
    else:
        transaction_type = sys.argv[1]
        print(type(transaction_type))
        check_system_time()
        get_deposit_history(transaction_type)

if __name__ == '__main__':
    sys.exit(main())