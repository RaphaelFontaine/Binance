import psycopg2
import sys
import json
from get_pwd import get_pwd



def initialize(pwd):
    try:
        conn = psycopg2.connect(
            user = "postgres",
            password = pwd,
            host = "localhost",
            port = "5433",
            database = "binance_data"
        )
        cur = conn.cursor()
        return (conn, cur)
    except (Exception, psycopg2.Error) as error :
        print ("Error when connecting to PostgreSQL", error)
    
def get_max_date(conn, cur):
    try:
        sql = """SELECT MAX(date) from operations"""
        cur.execute(sql)
        conn.commit()
        most_recent_date = cur.fetchone()[0]
        print("Getting last date in PostgreSQL database")
        if (most_recent_date != None):
            return most_recent_date
        else: 
            return -1

    except (Exception, psycopg2.Error) as error :
        print ("Error when getting last date in PostgreSQL", error)
        return -1

def delete_date(conn, cur, date):
    try:
        
        sql = """DELETE from operations WHERE date = %s;"""

        value = (date)
        cur.execute(sql, (value,))
        conn.commit()
        print("Deletion of a date in the PostgreSQL database")

    except (Exception, psycopg2.Error) as error :
        print ("Error when deleting a date in PostgreSQL", error)

def tri_dates_and_values(deposits_dates, deposits_values, withdrawals_dates, withdrawals_values):
    L1 = []
    L2 = []
    L3 = []
    len1 = len(deposits_dates)
    len2 = len(withdrawals_dates)

    print(deposits_values)
    print(withdrawals_values)

    k = 0
    i = 0
    while (k < len1 or i < len2):
        if (k < len1 and i < len2):
            if (deposits_dates[k] < withdrawals_dates[i] ):
                print(deposits_values[k])
                L1.append(deposits_dates[k])
                L2.append(deposits_values[k])
                L3.append(True)
                k += 1
            else:
                print(withdrawals_values[i])
                L1.append(withdrawals_dates[i])
                L2.append(withdrawals_values[i])
                L3.append(False)
                i +=1
        elif (k>= len1):
            L1.append(withdrawals_dates[i])
            L2.append(withdrawals_values[i])
            L3.append(False)
            i +=1
        else:
            L1.append(deposits_dates[k])
            L2.append(deposits_values[k])
            L3.append(True)
            k += 1

    

    print(L2)
    return (L1, L2, L3)

def send_bitcoin_data(conn, cur):

    data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/operations.json"
    with open(data_file, 'r') as f:
        operations_data = json.loads(f.read())
    
    deposits = operations_data['deposits']
    withdrawals = operations_data['withdrawal']

    deposits_dates = list(deposits.keys())
    deposits_values = list(deposits.values())

    withdrawals_dates = list(withdrawals.keys())
    withdrawals_values = list(withdrawals.values())

    dates, values, types = tri_dates_and_values(deposits_dates, deposits_values, withdrawals_dates, withdrawals_values)

    try:
        sql = """INSERT INTO operations (id, type, date, value) VALUES (%s,%s, %s, %s)"""
        rang = -1
        most_recent_date = get_max_date(conn, cur)
        if (most_recent_date != -1):
            most_recent_date = most_recent_date.strftime('%Y-%m-%d')
            rang = dates.index(most_recent_date)
        if (not rang == len(dates)-1):
            for k in range(rang+1, len(dates)):
                id = k +1
                date = dates[k]
                price = int(values[k])
                type = types[k]
                value = (id, type, date, price)
                print(value)
                cur.execute(sql, value)
                conn.commit()
            print("Data added with success in PostgreSQL database ")
        else:
            print("All datas have already been added")

    except (Exception, psycopg2.Error) as error :
        print ("Error when adding datas in PostgreSQL database : ", error)


def main():

    pwd = get_pwd()
    conn, cur = initialize(pwd)

    send_bitcoin_data(conn, cur)

    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("Connection to PostgreSQL closed")

if __name__ == '__main__':
    sys.exit(main())