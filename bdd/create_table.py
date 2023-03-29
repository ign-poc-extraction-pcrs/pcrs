from postgres import Postgres

p = Postgres()
p.connection()
p.create_table()
p.close_connection()