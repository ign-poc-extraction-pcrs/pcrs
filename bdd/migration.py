from postgres import Postgres

p = Postgres()
p.connection()
p.insert()
p.close_connection()