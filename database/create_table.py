import psycopg2
import sys
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


def create_bitcoin_table(conn, cur):

    try:
        
        sql = '''CREATE TABLE IF NOT EXISTS bitcoin(
            DATE DATE PRIMARY KEY NOT NULL,
            value FLOAT NOT NULL
        ); '''
        
        cur.execute(sql)
        conn.commit()
        print("Table created with succes in PostgreSQL")

    except (Exception, psycopg2.Error) as error :
        print ("Error when creating the table bitcoin in PostgreSQL", error)

def create_operations_table(conn, cur):

    try:
        sql = '''CREATE TABLE IF NOT EXISTS operations(
            id INT PRIMARY KEY NOT NULL,
            type BOOL,
            date DATE NOT NULL,
            value INT
        ); '''
        
        cur.execute(sql)
        conn.commit()
        print("Table created with succes in PostgreSQL")

    except (Exception, psycopg2.Error) as error :
        print ("Error when creating the table bitcoin in PostgreSQL", error)




def main():
    pwd = get_pwd()
    conn, cur = initialize(pwd)

    create_bitcoin_table(conn, cur)
    create_operations_table(conn, cur)

    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("Connection to PostgreSQL closed")

if __name__ == '__main__':
    sys.exit(main())