import os
from dotenv import load_dotenv
import psycopg2
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
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Erreur lors de la connexion à la base de données :", error)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE test (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                age INTEGER
            );
        """)
        self.connection.commit()
    
    def insert(self):
        try:
            # exemple d'insertion de données dans une table
            insert_query = "INSERT INTO test (name, age) VALUES ( %s, %s)"
            record_to_insert = ("value2", "value3")
            self.cursor.execute(insert_query, record_to_insert)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Erreur lors de l'insertion de données :", error)
    
    def close_connection(self):
        # fermeture de la connexion à la base de données
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connexion à la base de données fermée")