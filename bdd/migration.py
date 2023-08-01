from postgres import Postgres

p = Postgres()
p.connection()
# p.create_extension()
p.create_table("""
            CREATE EXTENSION postgis IF NOT EXIST;
            CREATE TABLE IF NOT EXISTS dalle (
            id serial PRIMARY KEY,
            nom VARCHAR(200) NOT NULL,
            geom geometry NOT NULL);
        """)

p.create_table("""
            CREATE EXTENSION postgis IF NOT EXIST;
            CREATE TABLE IF NOT EXISTS chantier (
            id serial PRIMARY KEY,
            bloc VARCHAR(200) NOT NULL,
            geom_chantier geometry NULL);
        """)

p.insert("dalle", "(nom, geom)", "nom", p.get_dalle_json("dalle")["dalles"])
p.insert("chantier", "(bloc, geom_chantier)", "bloc", p.get_dalle_json("chantier")["dalles"])
p.close_connection()