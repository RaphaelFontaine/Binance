import sys
import matplotlib.pyplot as plt
from get_wallet import *
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os
import time

DATE = "2021-10-10"
keys = get_keys()
api_key = keys[0]
api_secret = keys[1]

data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/wallet_value.json"

def liste_dates_jusqu_a_aujourd_hui(DATE):
    date = DATE
    aujourd_hui = time.strftime("%Y-%m-%d")
    dates = []

    taille = os.stat(data_file).st_size
    if (taille != 0):
        with open(data_file, 'r') as f:
            wallet_value_data = json.loads(f.read())
        old_dates = list(wallet_value_data.keys())
        date = old_dates[len(old_dates)-1]
    else : 
        date = DATE

    while date < aujourd_hui:
        date = datetime.strptime(date, '%Y-%m-%d')
        date = date + timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        dates.append(date)
    return dates

def wallet_value():

    dates = liste_dates_jusqu_a_aujourd_hui(DATE)

    if not dates:
        print("We already got every data in our json : wallet_value.json")
        return -1

    L = get_wallet_value(dates[0])
    all_cryptos_values = L[0]
    cryptos_trigram = L[1]
    print(all_cryptos_values)
    print(cryptos_trigram)
    taille = os.stat(data_file).st_size
    if (taille != 0):
        with open(data_file, 'r') as f:
            wallet_value_data = json.loads(f.read())
    else: 
        wallet_value_data = {}

    nbr_dates = len(dates)
    print(nbr_dates)
    nbr_cryptos = len(all_cryptos_values)
    print(nbr_cryptos)
    if (nbr_cryptos > 0):
        nbr_days = len(all_cryptos_values[0])
    else:
        print("The wallet does not contain any cryptos")
        return -1

    new_all_crypto_values = []
    for k in range(nbr_cryptos):
        if (len(all_cryptos_values[k]) != nbr_dates):
            print(f"Crypto {k} is not considered in our wallet value because we don\'t have enough past data")
        else:
            new_all_crypto_values.append(all_cryptos_values[k])

    nbr_cryptos = len(new_all_crypto_values)

    for k in range(nbr_days):
        print(k)
        json_day = {}
        for i in range(nbr_cryptos):
            print(i)
            trigram = cryptos_trigram[i]
            day_crypto_value = new_all_crypto_values[i][k]
            json_day[trigram] = day_crypto_value
        date = dates[k]
        wallet_value_data[date] = json_day
        print(date)

    with open(data_file, 'w') as f:
        json.dump(wallet_value_data, f, indent=4, sort_keys=True)
    return 0

def graph_wallet_value():
    with open(data_file, 'r') as f:
        wallet_value_data = json.loads(f.read())

    dates = list(wallet_value_data.keys())
    my_wallet_values = []
    
    for k in range(len(dates)):
        day_value = 0
        json_day = wallet_value_data[dates[k]]
        values = list(json_day.values())
        for i in range(len(values)):
            day_value = day_value + values[i]
        my_wallet_values.append(day_value)

    fig, ax = plt.subplots()
    dates = [datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in dates]
    ax.plot(dates, my_wallet_values)

    # Affichage du graphe
    plt.xlabel("Date")
    plt.ylabel("Wallet value")
    plt.title("Variation of my wallet value since October 2021")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # plt.show()

    aujourd_hui = datetime.now().strftime('%Y-%m-%d')
    plt.savefig('../data/wallet_value/'+aujourd_hui+'.png')

def main():
    liste_dates_jusqu_a_aujourd_hui(DATE)
    wallet_value()
    graph_wallet_value()


if __name__ == '__main__':
    sys.exit(main())