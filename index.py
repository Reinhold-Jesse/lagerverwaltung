from flask import Flask, render_template, request, redirect, escape, session, flash
from datetime import datetime
import os
from functionen import reinhold
from functionen import abed

# eigenes datanbank modul einbinden (Frank Hoffmann)
from functionen import datenbank

app = Flask(__name__)
# secret_key generator
#print(os.urandom(36))
app.secret_key = "\xeaR\xab\xdar\xc6\xcdDQO\xd1\xdaq\xff\xfaT\x91\xcf\xb9\n\x05t\xae-o jm\x84\xd5\x12\\x\x07u\xef"


@app.route("/")
def index():
    # Alle Artikeln anzeigen
    # übergibt die anfrage weiter das das Template

    #print('Startseite start')
    #print('Preis alle Artikel in der Datenbank: ', abed.getTotalPrice(), '€')
    # print(reinhold.date())
    #print('Startseite ende')
    temp = {
        'total_price': reinhold.germanPrice(abed.getTotalPrice())
    }

    return render_template('index.html', content=temp)


@app.route('/artikel')
def artikel_index():
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
    #print(content)

    return render_template('artikel/index.html', content=content)


@app.route('/artikel/create')
def artikel_create():
    # Eine neues Artikel anlegen
    return render_template('artikel/create.html')



@app.route('/artikel/store', methods=['POST'])
def artikel_store():
    #speichert die daten in die Datenbank
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
    sql = "INSERT INTO articels (item_number, title, description, price, inventory, created_at) VALUES ('"+item_number+"','"+title+"','"+description+"',"+price+","+inventory+",'"+str(datum)+"');"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    # return message
    flash(u'Artikel wurde erfolgreich gespeichert.', 'successe')

    return redirect('/artikel')



@app.route('/artikel/<int:id>', methods=['GET','POST'])
def artikel_edit_update(id):
    if request.method == 'POST':
        #Ein artikel update
        datum = datetime.now()

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
        sql = "UPDATE articels SET item_number='"+item_number+"', title='"+title+"', description='"+description+"', price='"+price+"', status='"+status+"', inventory='"+inventory+"', updated_at='"+str(updated_at)+"'  WHERE id='" + str(id) + "';"
        datenbank.anweisungAusfuehren(zeiger, sql)
        # eintrga speichern
        datenbank.anweisungCommit(connection)
        # Datenbank Verbindung schließen
        datenbank.verbindungSchliessen(connection)

        # return message
        flash(u'Artikel wurde erfolgreich gespeichert.', 'successe')

        # weiterleiten an die Artikel übersicht
        return redirect('/artikel')
    else:
        # Eine Artikel bearbeiten
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

        # übergibt die anfrage weiter das das Template
        return render_template('artikel/edit.html', content=content)



@app.route('/artikel/delete', methods=['POST'])
def artikel_delete():
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "DELETE FROM articels WHERE id='"+str(request.form['id'])+"';"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # eintrga speichern
    datenbank.anweisungCommit(connection)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)

    # return message
    flash(u'Artikel wurde erfolgreich gelöscht.', 'successe')

    # weiterleiten an die Artikel übersicht
    return redirect('/artikel')


@app.route('/logfile')
def logfile_index():
    # Zeigt eine Tabele von Logfile aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    #connection = datenbank.verbindungHerstellen()
    # cursor
    #zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    #sql = "SELECT * FROM articels"
    #datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = []
    #content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    #datenbank.verbindungSchliessen(connection)
    #print(content)

    return render_template('logfile/index.html', content=content)



@app.route('/order')
def order():
    # Zeigt eine Tabele von Artikeln aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    connection = datenbank.verbindungHerstellen()
    # cursor
    zeiger = datenbank.cursorErstellen(connection)
    # SQL anweisung
    sql = "SELECT * FROM articels WHERE inventory >= '1' AND status='1'"
    datenbank.anweisungAusfuehren(zeiger, sql)
    # Daten auslesen
    content = datenbank.ergebniseHolen(zeiger)
    # Datenbank Verbindung schließen
    datenbank.verbindungSchliessen(connection)
    # print(content)

    return render_template('order.html', content=content)




@app.route('/order/add', methods=['POST'])
def order_add():
    artikel_id = int(request.form['id'])
    count = int(request.form['count'])
    order = [
        {'id': artikel_id, 'count': count}
    ]

    session.modified = True
    if 'order' in session:
        session['order'] = reinhold.array_marge(session['order'], order)
        #print(isinstance(session['order'],list))
        '''
        for value in session['order']:
            print(' inhalt: ', value)
        '''
    else:
        session['order'] = order

    #print(session)

    # return message
    flash(u'Artikel wurde erfolgreich in Wahrenkorb gelegt.', 'successe')
    return redirect('/order')


@app.route('/car')
def car():
    car = []
    total_price = 0.00
    if 'order' in session:
        #Artikeln wurdern in der Session gefunden.

        for element in session['order']:
            # Datenbank Verbindung Herstellen
            connection = datenbank.verbindungHerstellen()
            # cursor
            zeiger = datenbank.cursorErstellen(connection)
            # SQL anweisung
            sql = "SELECT * FROM articels WHERE id='"+str(element['id'])+"' ;"
            datenbank.anweisungAusfuehren(zeiger, sql)
            # Daten auslesen
            content = datenbank.ergebnisHolen(zeiger)
            # Datenbank Verbindung schließen
            datenbank.verbindungSchliessen(connection)

            temp = {
                'count': element['count'],
                'articel': content
            }

            # fügt Artikel der Car variable
            car.append(temp)

            #gesammt preis ermitteln
            total = float(temp['count']) * float(temp['articel'][4])
            # übergibt + addiert den total an die gesammt total_price
            total_price += total


    # wahrenkorb anzeigen
    return render_template('car.html', content=car, total_price=total_price)

@app.route('/car/update', methods=['POST'])
def carUpdate():
    # Warenkorb wird aktualisiert
    # Achtung request form liefert strings werte zurück
    # deshalb wird es in integer umgewandelt
    # artikel ID
    artikel_id = int(request.form['id'])
    # neue anzahl
    new_count = int(request.form['count'])

    # liest den ganzen wahrenkorb aus der session['order]
    for index, item in enumerate(session['order']):
        # wenn die gesuchte id gefunden ist
        if item['id'] == artikel_id:
            # schreibt die neuen anzahlt in die variable
            session['order'][index]['count'] = new_count

    flash(u'Artikel wurde erfolgreich aktualisiert.', 'successe')
    return redirect('/car')



@app.route('/car/delete', methods=['POST'])
def carDelete():
    # löscht einen Artikel aus dem Wahrenkorb
    # holt die id aus den form
    artikel_id = int(request.form['id'])

    # liest den ganzen wahrenkorb aus der session['order]
    for index, item in enumerate(session['order']):
        # wenn die gesuchte id gefunden ist
        if item['id'] == artikel_id:
            # entfernt den artikel aus dem session = wahrenkorb by index
            session['order'].pop(index)

    flash(u'Artikel wurde erfolgreich aus dem Wahrenkorb entfernt.', 'successe')
    return redirect('/car')

# wahren korb erstellen
# if 'name' in session:
# session['name'] = wert
# maskieren / entwerten escape((session['name']))
# session werte überschreiben
# session.pop('name',None)
# wahrenkorb artikel löschen


if __name__ == '__main__':
    app.run(port=5000, debug=True)