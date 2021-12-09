from functionen import datenbank

def index():
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM logs"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    return content