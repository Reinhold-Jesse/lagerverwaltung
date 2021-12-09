from functionen import datenbank
from datetime import datetime
import json

def index():
    # Zeigt eine Tabele von Artikeln aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM orders"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)
    # print(content)

    return content

def edit(id):
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM orders WHERE id=" + str(id) + ";"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content


def update(request, id):
    datum = datetime.now()

    status = request.form['status']
    updated_at = str(datum)

    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "UPDATE orders SET status='"+str(status)+"', updated_at='"+updated_at+"' WHERE id='" + str(id) + "';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)


def delete(id):
    # löscht die Bestellung und aktualisiert die Artikeln im lager

    datum = datetime.now()
    updated_at = str(datum)

    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)

    #Bestellunge auswählen
    sql = "SELECT * FROM orders WHERE id=" + str(id) + ";"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    order = datenbank.ergebnisHolen(zeiger)
    # json decoder
    #print(json.loads(order[2]))
    #Lagerbestand aktualisieren
    for item in json.loads(order[2]):
        #LAGERSTAND AKTUALISIEREN
        # holt den Artikel aus der Datenbank
        sql = "SELECT * FROM articels WHERE id=" + str(item['id']) + ";"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # Daten auslesen
        artikel = datenbank.ergebnisHolen(zeiger)
        inventory = artikel[6] + item['count']

        #ARTIKEL UPDATE
        sql = "UPDATE articels SET status='" + str(1) + "', inventory='"+str(inventory)+"', updated_at='" + updated_at + "' WHERE id='" + str(item['id']) + "';"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # eintrga speichern
        datenbank.anweisungCommit(connection)

        #ENTNAHME LÖSCHEN
        # SQL anweisung
        sql = "DELETE FROM logs WHERE order_number='" + str(order[1]) + "' AND articels_id='"+str(item['id'])+"';"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # eintrga speichern
        print(datenbank.anweisungCommit(connection))


    #EINTRAG aus der Datenbank löschen
    # SQL anweisung
    sql = "DELETE FROM orders WHERE id='" + str(order[0]) + "';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)
