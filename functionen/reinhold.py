import locale, datetime
from functionen import datenbank

# deutsche preis darstellung
def germanPrice(price):
    # Deutsche schreibweise für preise
    locale.setlocale(locale.LC_ALL, 'de_DE')
    return locale.format_string('%.2f', price, True) #return 2.000,00

# add List || Dictionaries
def array_marge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

def date():
    # funktion liefert das aktuelle Datum mit Uhrzeit zurück
    return datetime.datetime.now() # return 2021-12-01 11:13:02.513106


def getTotalOrderPrice():
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM orders ;"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    total_price = 0
    for item in content:
        total_price += item[3]

    return total_price


def getCountAllArtikelsInTabel():
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT COUNT(*) FROM articels;"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content[0]

def getCountAllLogfilsInTabel():
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT COUNT(*) FROM logs;"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content[0]

def getCountAllOrdersInTabel():
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT COUNT(*) FROM orders;"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content[0]

def getLastRowId(tabele_name):
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    # zählt alle zeilen
    #sql = "SELECT COUNT(*) FROM "+tabele_name+";"
    sql = "SELECT MAX(id) FROM "+tabele_name+";"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebnisHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    if content[0] == None:
        return 0
    else:
        return content[0]


