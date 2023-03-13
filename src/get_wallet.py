from binance.client import Client
from get_keys import *
import requests
import datetime
import pandas as pd

keys = get_keys()
api_key = keys[0]
api_secret = keys[1]

# print(f'API Key : ', api_key, '\nSECRET KEY : ', api_secret)

client = Client(api_key, api_secret)

balances = client.get_account()['balances']

def get_crypto_value(TRIGRAM):
    TRIGRAM = TRIGRAM + "USDT"
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={TRIGRAM}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = float(data['price'])
        return price
    else:
        return None

def get_crypto_value_by_day(TRIGRAM, date):
    TRIGRAM = TRIGRAM + "USDT"
    try:
        data = Client().get_historical_klines(TRIGRAM, Client.KLINE_INTERVAL_1DAY, date)
        df = pd.DataFrame(data, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        df = df['open'].tolist()
        return df
    except:
        print(f"Erreur lors de la récupération des données historiques de {TRIGRAM}")
        return -1
            

def get_wallet_capitalization_by_crypto():
    positions = []
    wallet = {}
    r = 0
    for balance in balances:
        if float(balance['free']) + float(balance['locked']) > 0:
            asset = balance['asset']
            free = float(balance['free'])
            locked = float(balance['locked'])
            total = free + locked
            positions.append({'asset': asset, 'free': free, 'locked': locked, 'total': total})
    
    # Building json based on this format : {crypto1 : capitalization, crypto2 : capitalization, crypto3 : capitalization, ...}
    for p in positions:
        TRIGRAM = p['asset']
        value = get_crypto_value(TRIGRAM)
        if (value != None):
            capitalization = p['total'] * value
            if (capitalization>10):
                wallet[TRIGRAM] = capitalization
    return wallet

def get_wallet_value(date):
    positions = []
    all_cryptos_values = []
    cryptos_trigram = []
    
    for balance in balances:
        if float(balance['free']) + float(balance['locked']) > 0:
            asset = balance['asset']
            free = float(balance['free'])
            locked = float(balance['locked'])
            total = free + locked
            positions.append({'asset': asset, 'total': total})
    

    for p in positions:
        TRIGRAM = p['asset']
        cryptos_trigram.append(TRIGRAM)
        total = p['total']
        crypto_value_by_day = get_crypto_value_by_day(TRIGRAM, date)
        if (crypto_value_by_day != -1):
            for k in range(len(crypto_value_by_day)):
                crypto_value_by_day[k] = total * float(crypto_value_by_day[k])
            all_cryptos_values.append(crypto_value_by_day)

    return [all_cryptos_values, cryptos_trigram]
        


