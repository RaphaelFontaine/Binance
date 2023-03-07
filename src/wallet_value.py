import sys
import matplotlib.pyplot as plt
import numpy as np
from get_wallet import *
from datetime import datetime, timedelta
import matplotlib.dates as mdates

DATE = "01 OCTOBER 2021"

def liste_dates_jusqu_a_aujourd_hui(DATE):
    date = datetime.strptime(DATE, '%d %B %Y')

    aujourd_hui = datetime.now()
    dates = []

    while date <= aujourd_hui:
        dates.append(date.strftime('%d/%m/%Y'))
        date = date + timedelta(days=1)

    return dates

def wallet_repartition():

    my_wallet_values = []
    all_cryptos_values = get_wallet_value(DATE)

    dates = liste_dates_jusqu_a_aujourd_hui(DATE)
    dates = [datetime.strptime(date, '%d/%m/%Y') for date in dates]

    nbr_dates = len(dates)

    nbr_cryptos = len(all_cryptos_values)
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
        day_value = 0
        for i in range(nbr_cryptos):
            day_value = day_value + new_all_crypto_values[i][k]
        my_wallet_values.append(day_value)

    

    fig, ax = plt.subplots()
    ax.plot(dates, my_wallet_values)

    date_form = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(date_form)

    # Ajouter des labels pour les axes
    ax.set_xlabel('Time')
    ax.set_ylabel('My wallet valuation')

    # Afficher le graphique
    plt.xticks(rotation=45)
    plt.title("Evolution of my wallet value depending on time")
    aujourd_hui = datetime.now().strftime('%Y-%m-%d')
    plt.savefig('../data/wallet_value/'+aujourd_hui+'.png')


def main():
    wallet_repartition()


if __name__ == '__main__':
    sys.exit(main())