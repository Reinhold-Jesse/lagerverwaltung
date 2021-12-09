from flask import session
from functionen import datenbank
from datetime import datetime
from functionen import reinhold
import json


def index():
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM articels WHERE inventory >= '1' AND status='1';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content

def enter():
    datum = datetime.now()
    total_price = 0.00

    bestellnummer = str(datum.year) + str(datum.month) + str(int(reinhold.getLastRowId('orders')) + int(1))


    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)

    # holt aktikeln die ausgewählt wurden
    for item in session['order']:

        sql = "SELECT * FROM articels WHERE id= '" + str(item['id']) + "';"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # Daten auslesen
        articel = datenbank.ergebnisHolen(zeiger)

        # fasst die bestellung zusammen
        total_price += float(item['count'] * articel[4])

        # entnahme Protokolieren in logs Tabelle
        sql = "INSERT INTO logs (order_number, articels_id, title, pieces, created_at) VALUES ('" + bestellnummer + "','" + str(articel[0]) + "','" + articel[2] + "','" + str(item['count']) + "','" + str(datum) + "');"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # eintrga speichern
        datenbank.anweisungCommit(connection)

        # Artikel Lagerbestand aktualisieren
        neu_inventory = articel[6] - item['count']

        if neu_inventory > 1:
            sql = "UPDATE articels SET  inventory='" + str(neu_inventory) + "', updated_at='" + str(datum) + "'  WHERE id='" + str(articel[0]) + "';"
        else:
            sql = "UPDATE articels SET status='0',  inventory='" + str(neu_inventory) + "', updated_at='" + str(datum) + "'  WHERE id='" + str(articel[0]) + "';"

        datenbank.anweisungAusfuehren(zeiger, sql)
        datenbank.anweisungCommit(connection)

    # Bestellung in die Datenbank erfassen = orders
    sql = "INSERT INTO orders (order_number, order_articels, total_price, status, created_at) VALUES ('%s', '%s', '%s', '%s', '%s' );" % (str(bestellnummer), json.dumps(session['order']), total_price, 0, datum)
    print(sql)
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)

    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    # Session inhalte löschen
    session.pop('order', None)
    # löscht alle session inhalte
    # session.clear()
