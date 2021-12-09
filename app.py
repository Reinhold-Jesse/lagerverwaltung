from flask import Flask, render_template, request, redirect, escape, session, flash
from datetime import datetime
import os
import secrets
from functionen import reinhold
from Controllers import ArticelController, LogfileController, ShopController, CarController, OrderController


# eigenes datanbank modul einbinden (Frank Hoffmann)
from functionen import datenbank

app = Flask(__name__)



# secret_key generator
#print(secrets.token_hex())
#print(os.urandom(36))
app.secret_key = "b94c563fee2960ba65267b0b4b5ffd4adf767548da261dc9e2138807f51ebe9c"


@app.route("/")
def index():
    # übergibt die anfrage weiter das das Template
    temp = {
        'total_price': reinhold.germanPrice(reinhold.getTotalOrderPrice()),
        'total_articls': reinhold.getCountAllArtikelsInTabel(),
        'total_logfile': reinhold.getCountAllLogfilsInTabel(),
        'total_orders': reinhold.getCountAllOrdersInTabel(),
    }

    print(reinhold.getLastRowId('orders'))
    return render_template('index.html', content=temp)


@app.route('/artikel')
def artikel_index():
    content = ArticelController.index()
    return render_template('artikel/index.html', content=content)


@app.route('/artikel/create')
def artikel_create():
    # Eine neues Artikel anlegen
    return render_template('artikel/create.html')


@app.route('/artikel/store', methods=['POST'])
def artikel_store():
    #Speichert den Neuen Artikel in die Datenbank
    ArticelController.store(request)
    # return message
    flash(u'Artikel wurde erfolgreich gespeichert.', 'successe')
    return redirect('/artikel')



@app.route('/artikel/<int:id>', methods=['GET','POST'])
def artikel_edit_update(id):
    # entwerten
    id = escape(id)

    if request.method == 'POST':
        #Ein artikel update
        ArticelController.update(request, id)
        # return message
        flash(u'Artikel wurde erfolgreich gespeichert.', 'successe')
        # weiterleiten an die Artikel übersicht
        return redirect('/artikel')
    else:
        # Eine Artikel bearbeiten
        content = ArticelController.edit(id)
        # übergibt die anfrage weiter das das Template
        return render_template('artikel/edit.html', content=content)



@app.route('/artikel/delete', methods=['POST'])
def artikel_delete():
    #löscht den Artikel aus der Datenbank per ID
    ArticelController.delete(request.form['id'])
    # return message
    flash(u'Artikel wurde erfolgreich gelöscht.', 'successe')
    # weiterleiten an die Artikel übersicht
    return redirect('/artikel')


@app.route('/logfile')
def logfile_index():
    # Zeigt eine Tabele von Logfile aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    content = LogfileController.index()
    return render_template('logfile/index.html', content=content)



@app.route('/shop')
def shop_index():
    # Zeigt eine Tabele von Artikeln aus der Datenbank
    # hier holen wir die daten aus der Datenbank
    # Datenbank Verbindung Herstellen
    content = ShopController.index()

    return render_template('order.html', content=content)


@app.route('/order')
def order_index():
    content = OrderController.index()
    return render_template('order/index.html', content=content)

@app.route('/order/<int:id>', methods=['GET','POST'])
def order_edit_update(id):
    # entwerten
    id = escape(id)

    if request.method == 'POST':
        #Ein artikel update
        OrderController.update(request, id)
        # return message
        flash(u'Bestell Status wurde geändert', 'successe')
        # weiterleiten an die Artikel übersicht
        return redirect('/order')
    else:
        # Eine Artikel bearbeiten
        content = OrderController.edit(id)
        # übergibt die anfrage weiter das das Template
        return render_template('order/edit.html', content=content)



@app.route('/order/delete', methods=['POST'])
def order_delete():
    #löscht den Artikel aus der Datenbank per ID
    OrderController.delete(request.form['id'])

    # return message
    flash(u'Bestellung wurde erfolgreich gelöscht.', 'successe')
    # weiterleiten an die Artikel übersicht
    return redirect('/order')


@app.route('/order/enter')
def order_enter():
    # bestellung erfassen und die session löschen
    ShopController.enter()
    # return message
    flash(u'Bestellung wurde erfolgreich erfasst.', 'successe')
    return redirect('/car')


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


@app.route('/car/add', methods=['POST'])
def car_add():
    # Artikel in den Wahrenkorb legen
    CarController.add(request)
    # return message
    flash(u'Artikel wurde erfolgreich in Wahrenkorb gelegt.', 'successe')
    return redirect('/shop')


@app.route('/car/update', methods=['POST'])
def car_update():
    # Warenkorb wird aktualisiert
    # Achtung request form liefert strings werte zurück
    # deshalb wird es in integer umgewandelt
    CarController.update(request)
    # return message
    flash(u'Artikel wurde erfolgreich aktualisiert.', 'successe')
    return redirect('/car')



@app.route('/car/delete', methods=['POST'])
def car_delete():
    # löscht einen Artikel aus dem Wahrenkorb
    CarController.delete(request)

    flash(u'Artikel wurde erfolgreich aus dem Wahrenkorb entfernt.', 'successe')
    return redirect('/car')



if __name__ == '__main__':
    app.run(port=5000, debug=True)