import sqlite3


# Datenbankmodul / Zugriff fuer sqlite3
datenbank = "datenbank/lagerverwaltung.db"


def verbindungHerstellen():
 """Verbindung zur SQLite-DB herstellen"""
 try:
  connection = sqlite3.connect(datenbank)
  return connection
 except Error as e:
  print(e)
  return None


def verbindungSchliessen(verbindungsId):
 """Verbindung zur SQLite-DB beenden"""
 if verbindungsId:
  verbindungsId.close()
 return


def cursorErstellen(verbindungsId):
 """Zugriffscursor holen"""
 return verbindungsId.cursor()


def anweisungAusfuehren(cursor, sql):
 """SQL-Anweisung ausfuehren"""
 if cursor:
  if sql:
   cursor.execute(sql)

def anweisungCommit(verbindungsId):
 verbindungsId.commit()
 return

def ergebniseHolen(cursor):
 """Hole das Ergebnis der SQL-Anfrage
 return : mehrere ergebnisse list->tupel"""
 if cursor:
  zeilen = cursor.fetchall()
  return zeilen
 else:
  return []

def ergebnisHolen(cursor):
 """Hole das Ergebnis der SQL-Anfrage
 return : 1 Tupel"""
 if cursor:
  zeilen = cursor.fetchone()
  return zeilen


# benötigten funktionen
# return SQL als dictionaries stat Tupel
# in mehreren und einzeln
