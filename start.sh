#!/bin/bash

logs="/Users/raphaelfontaine/Documents/GIT/Binance/logs/"
date=$(date +%Y-%m-%d)

if [ "$#" -eq 0 ]; 
    then
        echo "------ MY WALLET REPARTITION DIAGRAM ------"

        logs_path=$logs"wallet_repartition/"$date".log"

        cd /Users/raphaelfontaine/Documents/GIT/Binance/src
        /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_repartition.py >> $logs_path

        echo "GO TO  /data/wallet_repartition TO SEE IT"


        echo "------ MY WALLET VALUE DIAGRAM ------"

        logs_path=$logs"wallet_value/"$date".log"

        cd /Users/raphaelfontaine/Documents/GIT/Binance/src
        /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_value.py >> $logs_path

        echo "GO TO  /data/wallet_value TO SEE IT"

        echo "------ BITCOIN VALUE DIAGRAM ------"

        logs_path=$logs"bitcoin/"$date".log"

        cd /Users/raphaelfontaine/Documents/GIT/Binance/src
        /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 bitcoin.py >> $logs_path

        echo "GO TO  /data/bitcoin TO SEE IT"

        echo "------ BITCOIN VALUE DIAGRAM ------"

        logs_path=$logs"bitcoin/"$date".log"

        cd /Users/raphaelfontaine/Documents/GIT/Binance/src
        /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 bitcoin.py >> $logs_path

        echo "GO TO  /data/bitcoin TO SEE IT"

        echo "------ DEPOSITS DIAGRAM ------"

        logs_path=$logs"operations/"$date".log"

        cd /Users/raphaelfontaine/Documents/GIT/Binance/src
        /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 get_operations.py 0 >> $logs_path

        echo "GO TO  /data/operations/deposits TO SEE IT"

elif [ "$#" -eq 1 ]; 
    then
        if [ $1 == "v" ];
            then 
                echo "------ MY WALLET VALUE DIAGRAM ------"

                logs_path=$logs"wallet_value/"$date".log"

                cd /Users/raphaelfontaine/Documents/GIT/Binance/src
                /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_value.py >> $logs_path

                echo "GO TO  /data/wallet_value TO SEE IT"

        elif [ $1 == "r" ];
            then 
                echo "------ MY WALLET REPARTITION DIAGRAM ------"

                logs_path=$logs"wallet_repartition/"$date".log"
                echo $logs_path

                cd /Users/raphaelfontaine/Documents/GIT/Binance/src
                /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 wallet_repartition.py >> $logs_path

                echo "GO TO  /data/wallet_repartition TO SEE IT"

        elif [ $1 == "b" ];
            then 
                echo "------ BITCOIN VALUE DIAGRAM ------"

                logs_path=$logs"bitcoin/"$date".log"

                cd /Users/raphaelfontaine/Documents/GIT/Binance/src
                /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 bitcoin.py >> $logs_path

                echo "GO TO  /data/bitcoin TO SEE IT"

        elif [ $1 == "d" ];
            then 
                echo "------ DEPOSITS DIAGRAM ------"

                logs_path=$logs"operations/"$date".log"

                cd /Users/raphaelfontaine/Documents/GIT/Binance/src
                /Users/raphaelfontaine/Documents/GIT/Binance/venv_binance/bin/python3 get_operations.py 0 >> $logs_path

                echo "GO TO  /data/operations/deposits TO SEE IT"

        else
            echo "Enter one of the following argument depending on what diagraph you want \n - r : repartition of yor wallet \n - v : value of your wallet "
        fi

else
    echo -e "Enter zero or one argument. If you enter one arg, enter of the following argument depending on what diagramm you want \n - r : repartition of yor wallet \n - v : value of your wallet \n - b : bitcoin value evolution \n - d : deposits operations in the account "
fi
