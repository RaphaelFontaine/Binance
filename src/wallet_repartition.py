import sys
import matplotlib.pyplot as plt
import numpy as np
from get_wallet import *
from datetime import datetime, timedelta


def wallet_repartition(wallet):
    crypto_names = list(wallet.keys())
    crypto_values = list(wallet.values())

    # Pie chart building
    fig, ax = plt.subplots()
    wedges, labels = ax.pie(crypto_values,  startangle=90, labels=None)

    # Add percentages as labels outside graph
    labels = ['{0} - {1:1.1f}%'.format(crypto_names[i], crypto_values[i]/sum(crypto_values)*100) for i in range(len(crypto_names))]
    plt.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    
    aujourd_hui = datetime.now().strftime('%Y-%m-%d')
    plt.title('My Crypto Wallet repartition : ' + aujourd_hui)
    # plt.show()
    plt.tight_layout()
    plt.savefig('../data/wallet_repartition/'+aujourd_hui+'.png')

def main():
    wallet = get_wallet_capitalization_by_crypto()
    wallet_repartition(wallet)


if __name__ == '__main__':
    sys.exit(main())