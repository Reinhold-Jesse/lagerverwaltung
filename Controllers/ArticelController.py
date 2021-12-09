from Models import Articel
from functionen import datenbank
from datetime import datetime

def index():
    # Zeigt eine Tabele von Artikeln aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM articels"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)
    # print(content)

    return content


def store(request):
    datum = datetime.now()

    item_number = request.form['item_number']
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    inventory = request.form['inventory']

    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "INSERT INTO articels (item_number, title, description, price, inventory, created_at) VALUES ('" + item_number + "','" + title + "','" + description + "'," + price + "," + inventory + ",'" + str(datum) + "');"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)


def edit(id):
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM articels WHERE id=" + str(id) + ";"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content


def update(request,id):
    datum = datetime.now()
    print(request)
    item_number = request.form['item_number']
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    status = request.form['status']
    inventory = request.form['inventory']
    updated_at = datum

    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "UPDATE articels SET item_number='" + item_number + "', title='" + title + "', description='" + description + "', price='" + price + "', status='" + status + "', inventory='" + inventory + "', updated_at='" + str(updated_at) + "'  WHERE id='" + str(id) + "';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)


def delete(id):
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "DELETE FROM articels WHERE id='" + str(id) + "';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)