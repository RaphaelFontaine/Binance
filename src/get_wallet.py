from binance.client import Client
from get_keys import *
import requests

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

def get_wallet():
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
