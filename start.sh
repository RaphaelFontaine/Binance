#!/bin/bash

echo "------ MY WALLET REPARTITION DIAGRAM ------"

cd /Users/raphaelfontaine/Documents/GIT/Binance/src
/Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_repartition.py

echo "GO TO  /data/wallet_repartition TO SEE IT"


echo "------ MY WALLET VALUE DIAGRAM ------"

cd /Users/raphaelfontaine/Documents/GIT/Binance/src
/Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_value.py

echo "GO TO  /data/wallet_value TO SEE IT"
