import sqlite3
import datetime

# Datenbank erstellen
# Datenbank wird angelegt wenn sie nicht vorhanden ist
datenbank = "datenbank/lagerverwaltung.db"

verbindung = sqlite3.connect(datenbank)

zeiger = verbindung.cursor()

# Tabelen erstellen
# Artikeln Tabelle erstellen

sql = """CREATE TABLE IF NOT EXISTS articels (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    item_number VARCHAR(30),
    title VARCHAR(191),
    description TEXT NOT NULL,
    price FLOAT,
    status INTEGER(1) DEFAULT TRUE,
    inventory INTEGER,
    created_at timestamp,
    updated_at timestamp
);"""

zeiger.execute(sql)


# Dummy Artikeln anlegen
#date = '2021.11.24 15:51:00'
date = datetime.datetime.now()
articels = [
    ('100010', 'Soken', 'beschreibung soken', 12.99, 50, date),
    ('100020', 'Unterwäsche', 'beschreibung unterwäsche', 7.99, 150, date),
    ('100030', 'T-Shirt', 'beschreibung t-shirt', 12.99, 80, date),
    ('100040', 'Hose', 'beschreibung unterwäsche', 49.00, 20, date),
    ('100050', 'Schuhe', 'beschreibung schuhe', 99.99, 7, date)
]

zeiger.executemany("""INSERT INTO articels (item_number, title, description, price, inventory, created_at) VALUES (?,?,?,?,?,?)""", articels)
# speichern in die Datenbank
verbindung.commit()


# Datenbank Verbindung schließen
verbindung.close()