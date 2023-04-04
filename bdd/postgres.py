import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error

class Postgres:
    def __init__(self) -> None:
        pass

    def connection(self):
        load_dotenv()
        # informations de connexion à la base de données
        host = os.environ.get('HOST')
        database = os.environ.get('POSTGRES_DB')
        user = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        # connexion à la base de données
        try:
            self.connection = psycopg2.connect(user=user, password=password, host=host, database=database, port="5432")
            
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        except (Exception, Error) as error:
            print("Erreur lors de la connexion à la base de données :", error)

    def create_extension(self):
        self.connection.autocommit = True 
        sql = '''CREATE EXTENSION IF NOT EXISTS postgis''';
        self.cursor.execute(sql)


    def create_table(self, requete):
        self.cursor.execute(requete)
        self.connection.commit()
    
    def insert(self, table, column, column_not_duplicate, data):
        try:
            for d in data:
                self.cursor.execute(f"SELECT {column_not_duplicate} FROM {table} WHERE {column_not_duplicate} = '{d[column_not_duplicate]}'")
                # si la données n'est pas déjà en base on ne l'insere pas
                if not len(self.cursor.fetchall()) > 0:
                    requete = f"INSERT INTO {table} {column} VALUES (%s, %s)"
                    content = tuple(d.values())
                    self.cursor.execute(requete, content)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Erreur lors de l'insertion de données :", error)
    
    def close_connection(self):
        # fermeture de la connexion à la base de données
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connexion à la base de données fermée")