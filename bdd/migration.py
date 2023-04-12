from postgres import Postgres

p = Postgres()
p.connection()
p.create_extension()
p.create_table("""
            CREATE TABLE IF NOT EXISTS testt (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                age INTEGER,
                geom_chantier geometry NULL
            );
        """)
p.insert("testt", "(name, age)", "name", [{"name": "cedric", "age": 65},{"name": "vic", "age": 24}])
p.close_connection()