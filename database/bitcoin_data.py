import psycopg2
import sys
import json
import datetime

def initialize():
    try:
        conn = psycopg2.connect(
            user = "postgres",
            password = "admin",
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
        sql = """SELECT MAX(date) from bitcoin"""
        cur.execute(sql)
        conn.commit()
        most_recent_date = cur.fetchone()[0]
        print("Getting last date in PostgreSQL database")
    
        #fermeture de la connexion à la base de données
        cur.close()
        conn.close()
        print("Connection PostgreSQL closed")
        return most_recent_date

    except (Exception, psycopg2.Error) as error :
        print ("Error when getting last date in PostgreSQL", error)
        return -1

def delete_date(conn, cur, date):
    try:
        
        sql = """DELETE from bitcoin WHERE date = %s;"""

        value = (date)
        cur.execute(sql, (value,))
        conn.commit()
        print("Deletion of a date in the PostgreSQL database")

        cur.close()
        conn.close()
        print("Connection PostgreSQL closed")

    except (Exception, psycopg2.Error) as error :
        print ("Error when deleting a date in PostgreSQL", error)

def send_bitcoin_data(conn, cur):

    data_file = "/Users/raphaelfontaine/Documents/GIT/Binance/data/JSON_DATA/bitcoin_values.json"
    with open(data_file, 'r') as f:
        bitcoin_data = json.loads(f.read())
    dates = list(bitcoin_data.keys())
    values = list(bitcoin_data.values())

    try:
        sql = """INSERT INTO bitcoin (date, value) VALUES (%s,%s)"""

        most_recent_date = get_max_date(conn, cur)
        most_recent_date = most_recent_date.strftime('%Y-%m-%d')
        if (most_recent_date != -1):
            rang = dates.index(most_recent_date)
        if (not rang == len(dates)-1):
            for k in range(rang+1, len(dates)):
                date = dates[k]
                price = values[k]
                value = (date, price)
                cur.execute(sql, value)
                conn.commit()
            print("Data added with success in PostgreSQL database")
        else:
            print("All datas have already been added")
    
        cur.close()
        conn.close()
        print("Connection PostgreSQL closed")

    except (Exception, psycopg2.Error) as error :
        print ("Error when adding datas in PostgreSQL database", error)

def main():
    conn, cur = initialize()
    send_bitcoin_data(conn, cur)

if __name__ == '__main__':
    sys.exit(main())