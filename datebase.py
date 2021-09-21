import sqlite3 as sql


db = sql.connect('countries.db')

cursor = db.cursor()


cursor.executescript('''
CREATE TABLE IF NOT EXISTS pogoda(
pogoda_id INTEGER PRIMARY KEY AUTOINCREMENT,
city TEXT,
weather TEXT,
temp TEXT
);

CREATE TABLE IF NOT EXISTS info(
country_id INTEGER PRIMARY KEY AUTOINCREMENT,
country TEXT,
capital TEXT,
region TEXT,
area TEXT
);
''')

db.commit()
db.close()