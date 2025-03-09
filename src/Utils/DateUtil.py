from datetime import datetime, timedelta

DATE_FMT = "%d.%m.%Y"


"""
Berechnet die Relative Woche für den Parser

Attribute:
    start_week: Startdatum
    current_week: Aktuelle Woche
"""
def get_relative_week(start_week, current_week):
    return current_week - start_week + 1

"""
Berechnet die Kalenderwoche aus einem Datum

Attribute:
    date_str: Datum als String
"""
def get_week_from_date(date):
    return datetime.strptime(date, "%d.%m.%Y").isocalendar()[1]

"""
Berrechnet aus einem Datum und einen Offset das Datum vom Montag und vom Freitag

Attribute:
    start_week: Datum zum berechnen
    current_week: Offset der woche 
"""
def get_week_range(start_date, week_offset):
    #Wandelt des start_date string in ein datetime typen um
    start = datetime.strptime(start_date, DATE_FMT)
    #Berechnet wie viele Tage vorher der Montag ist
    days_to_monday = (start.weekday() - 0) % 7
    #Holt sich das Datum des Montags mit berücksichtigung des Offsets
    start_of_week = start - timedelta(days=days_to_monday) + timedelta(weeks=week_offset)
    #Holt sich das Datum des Freitags der Woche basierend auf dem Datum des Montags
    end_of_week = start_of_week + timedelta(days=(4 - start_of_week.weekday()) % 7)
    return start_of_week.strftime(DATE_FMT), end_of_week.strftime(DATE_FMT)