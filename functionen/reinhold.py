import locale, datetime

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