from flask import session
from functionen import reinhold


def add(request):
    # Artikel in den wahrenkorb legen
    artikel_id = int(request.form['id'])
    count = int(request.form['count'])
    order = [
        {'id': artikel_id, 'count': count}
    ]

    session.modified = True
    if 'order' in session:
        session['order'] = reinhold.array_marge(session['order'], order)
    else:
        session['order'] = order


def update(request):
    # Artikel im Wahrenkorb aktualisieren
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


def delete(request):
    # Artikel aus dem Wahrenkorb löschen
    # holt die id aus den form
    artikel_id = int(request.form['id'])

    # liest den ganzen wahrenkorb aus der session['order]
    for index, item in enumerate(session['order']):
        # wenn die gesuchte id gefunden ist
        if item['id'] == artikel_id:
            # entfernt den artikel aus dem session = wahrenkorb by index
            session['order'].pop(index)
