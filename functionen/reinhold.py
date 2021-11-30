import locale

# deutsche preis darstellung
def germanPrice(price):
    locale.setlocale(locale.LC_ALL, 'de_DE')
    return locale.format_string('%.2f', price, True)

# add List || Dictionaries
def array_marge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False