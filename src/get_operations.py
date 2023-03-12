import hashlib
import hmac
import requests
import json
import time
import datetime as dt
from get_wallet import *
import os
import sys
import matplotlib.pyplot as plt

keys = get_keys()
api_key = keys[0]
api_secret = keys[1]
exchanger_api_key = '4bqH7ZuctKO8qM5y10Mdgw46jVMbesYq'

DATE = "2021-09-01"

data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/operations.json"

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

    taille = os.stat(data_file).st_size

    if (taille != 0):
        with open(data_file, 'r') as f:
            operations_data = json.loads(f.read())
        if (transaction_type == "0"):
            operations = operations_data["deposits"]
        else:
            operations = operations_data["withdrawal"]
        
        if not not operations:
            old_dates = list(operations.keys())
            ms = date_to_ms(old_dates[len(old_dates)-1])
        else: 
            ms = date_to_ms(DATE)
    else : 
        ms = date_to_ms(DATE)
        operations_data = {
            "deposits" : {},
            "withdrawal" : {}
        }
        

    url = "https://api.binance.com/sapi/v1/fiat/orders"

    timestamp = int(dt.datetime.now().timestamp() * 1000)
    if (transaction_type == "0"):
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
    for deposit in deposits:
        status = deposit['status']
        if (status == 'Successful'):
            amount = float(deposit['indicatedAmount'])
            date = deposit['createTime']
            date = dt.datetime.fromtimestamp(date/1000)
            date = date.strftime('%Y-%m-%d')
            if (transaction_type == "0"):
                operations_data["deposits"][date] = amount
            else:
                operations_data["withdrawal"][date] = amount

    with open(data_file, 'w') as f:
        json.dump(operations_data, f, indent=4, sort_keys=True)
    return 0

def graph_operations(transaction_type):

    with open(data_file, 'r') as f:
        operations_data = json.loads(f.read())
    
    if (transaction_type == "0"):
        operations = operations_data["deposits"]
        title = "Deposits since creation of the account"
    else:
        operations = operations_data["withdrawal"]
        title = "Withdrawals since creation of the account"
    
    cumulative_sum = 0
    cumulative_data = {}

    for date, value in operations.items():
        cumulative_sum += value
        cumulative_data[date] = cumulative_sum

    x = list(cumulative_data.keys())
    y = list(cumulative_data.values())

    dates = list(operations.keys())
    values = list(operations.values())

    plt.bar(x, y)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for i, value in enumerate(y):
        plt.text(i, value, int(value), ha='center', va='bottom')
    
    aujourd_hui = dt.datetime.now().strftime('%Y-%m-%d')
    if (transaction_type == "0"):
        name_file = "deposits/" + aujourd_hui
    else:
        name_file = "withdrawals/" + aujourd_hui
    plt.savefig('../data/operations/'+name_file+'.png')
    # plt.show()

def main():
    if (len(sys.argv) == 1):
        print("Enter an arg : \n - 0 : deposits \n - 1 withdrawals")
        return 0
    else:
        transaction_type = sys.argv[1]
        check_system_time()
        get_deposit_history(transaction_type)
        graph_operations(transaction_type)

if __name__ == '__main__':
    sys.exit(main())