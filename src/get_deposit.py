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

DATE = "2022-01-01"

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

def get_deposit_history():

    # ms = get_ms_since_date(DATE)
    # print(ms)
    ms = date_to_ms(DATE)
    print(ms)


    url = "https://api.binance.com/sapi/v1/fiat/orders"

    timestamp = int(dt.datetime.now().timestamp() * 1000)
    params = {'transactionType' : '0', 'timestamp': timestamp, 'beginTime' : ms} 
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
        print(status)
        if (status == 'Successful'):
            amount = deposit['indicatedAmount']
            print(amount)
            total_deposit = total_deposit + float(amount)
    print(total_deposit)
        # deposit_time = dt.datetime.fromtimestamp(int(deposit['insertTime']) / 1000)
        # if deposit_time < dt.datetime.strptime(DATE, '%Y-%m-%d'):
        #     continue
        # deposit_amount = float(deposit['amount'])
        # deposit_asset = deposit['asset']
        # print(f"{deposit_time}: {deposit_amount} {deposit_asset}")
    

def main():
    check_system_time()
    get_deposit_history()


if __name__ == '__main__':
    sys.exit(main())