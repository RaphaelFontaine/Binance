import psycopg2

try:
    conn = psycopg2.connect(
          user = "postgres",
          password = "admin",
          host = "localhost",
          port = "5433",
          database = "binance_data"
    )
    cur = conn.cursor()

    sql = '''CREATE TABLE bitcoin(
        DATE DATE PRIMARY KEY NOT NULL,
        value FLOAT NOT NULL
      ); '''
    
    cur.execute(sql)
    conn.commit()
    print("Table créée avec succès dans PostgreSQL")
  
    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")

except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la création du table PostgreSQL", error)