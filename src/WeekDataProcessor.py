from datetime import datetime, timedelta
from typing import List, Tuple

import pandas as pd

from src.ConfigManager import ConfigManager
from src.WordTemplate import WordTemplate


class WeekDataProcessor:
    """Organisiert die CSV-Daten nach Wochen und füllt die Vorlage mit entsprechenden Werten aus."""

    """
    Initialisiert den WeekDataProcessor.

    Parameter:
    - logger: Logger-Objekt zum Protokollieren von Ereignissen und Fehlern.
    - settings: Konfigurationseinstellungen für die Anwendung.
    - document: Eine WordTemplate-Instanz, die das Word-Dokument repräsentiert.
    - data: Pandas DataFrame, der die CSV-Daten enthält.
    """
    def __init__(self, logger, CM : ConfigManager, document: WordTemplate, data: pd.DataFrame):
        self.logger = logger
        self.CM = CM
        self.document = document
        self.data = data
        self.weeks_data = self.initialize_weeks_data()

    """
    Berechnet die Kalenderwoche aus einem gegebenen Datum im Format 'dd.mm.yyyy'.
    """
    def get_week(self, date_str: str) -> int:
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").isocalendar()[1]
        except ValueError as e:
            # Protokolliert, wenn ein Datumswert ungültig ist.
            self.logger.error(f"Fehler beim Parsen des Datums '{date_str}': {e}")
            return -1  # Gibt -1 zurück, um Fehler bei der Wochenberechnung zu kennzeichnen.


    """
    Bestimmt den Typ der Tätigkeit basierend auf den CSV-Eingaben.

    Parameter:
    - activity: Beschreibung der Tätigkeit.

    Rückgabewert:
    - Ein String, der den Tätigkeitstyp beschreibt oder eine Standardnachricht bei unbekannten Tätigkeiten.
    """
    def get_activity_type(self, activity: str) -> str:
        if activity in self.CM.get_activitys():
            return self.CM.get_activitys()[activity]
        else:
            return self.CM.get_activitys()['NA']

    """
    Initialisiert und organisiert die Daten nach Kalenderwochen, wobei jeder Tag mit zugehörigen Tätigkeitsbeschreibungen
    erfasst wird und fehlende Tage mit Platzhaltern ergänzt werden.

    Rückgabewert:
    - Ein Dictionary mit der Wochenanzahl als Schlüssel und einer Liste von Tagesdaten als Wert.
    """
    def initialize_weeks_data(self):
        weeks_data = {}
        start_week = self.get_week(self.data['Datum'].iloc[0])

        # Iteriert durch jede Zeile des DataFrames und organisiert die Einträge nach relativen Wochen.
        for _, row in self.data.iterrows():
            date = row['Datum']
            current_week = self.get_week(date)
            relative_week = current_week - start_week + 1

            # Erzeugt einen Eintrag für den aktuellen Tag in der Woche.
            row_entry = {
                row['Tag'].upper(): {
                    "Art": self.get_activity_type(row['Tätigkeitsbeschreibung'].upper()),
                    "Inhalt": row.get('Beschreibung', ''),
                }
            }
            # Fügt den Eintrag der entsprechenden relativen Woche hinzu.
            weeks_data.setdefault(relative_week, []).append(row_entry)

        # Ergänzt fehlende Tage (z.B. wenn in einer Woche kein Eintrag für jeden Tag vorhanden ist).
        for week, entries in weeks_data.items():
            existing_days = {tag for entry in entries for tag in entry.keys()}
            missing_days = set(self.CM.get_work_days()) - existing_days
            for day in missing_days:
                # Fügt einen leeren Eintrag für den fehlenden Tag hinzu.
                entries.append({day: {"Art": "", "Inhalt": ""}})
                self.logger.warning(self.CM.get_error_messages()['missing_days'].format(day=day, week=week))

        return weeks_data



    """
    Verarbeitet Platzhalter für die gesamte Woche und ersetzt sie in der Word-Vorlage.

    Parameter:
    - week: Die relative Woche, die bearbeitet wird.
    - entries: Eine Liste von Tagesdaten für die Woche.
    """
    def process_week_placeholders(self, week, entries):
        # Berechnet Start- und Enddatum für die Woche basierend auf dem Startdatum der CSV-Daten.
        start_date, end_date = self.calculate_week_range(self.data['Datum'][0], week - 1)
        general_placeholders = {
            '{NAME}': self.CM.get_name(),
            '{ABJ}': self.CM.get_year(),
            f'{{DATUM_START{week}}}': start_date,
            f'{{DATUM_ENDE{week}}}': end_date
        }

        # Ersetzt allgemeine Platzhalter in jeder Tabelle des Dokuments.
        for table in self.document.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    # Ersetzt allgemeine Platzhalter (wie Name und Jahr).
                    self.document.replace_general_placeholders(cell, general_placeholders)
                    for day in self.CM.get_work_days():
                        # Ersetzt spezifische Platzhalter für jeden Tag der Woche.
                        day_data = next((entry.get(day, {}) for entry in entries if day in entry), {})
                        self.replace_placeholders_for_day(cell, day, week, day_data)

    """
    Ersetzt spezifische Platzhalter für einen Tag in einer Woche innerhalb einer Zelle.

    Parameter:
    - cell: Die Zelle im Word-Dokument, in der die Platzhalter ersetzt werden sollen.
    - day: Der Tag, für den die Platzhalter ersetzt werden sollen (z.B. 'Montag').
    - week: Die relative Woche.
    - data: Dictionary mit 'Art' und 'Inhalt' für die Tätigkeiten des Tages.
    """
    def replace_placeholders_for_day(self, cell, day, week, data):

        # Platzhalter für den Inhalt, die Stunden und die Art der Tätigkeit.
        placeholder_content = f"{{{day}_INHALT{week}}}"
        placeholder_hours = f"{{{day}_STUNDEN{week}}}"
        placeholder_type = f"{{{day}_ART{week}}}"

        # Formatierung des Inhalts und Anpassung der Tätigkeit.
        content = self.format_content(data.get('Inhalt', ''))
        data['Art'] = 'Berufsschule' if 'Berufsschule' in data.get('Inhalt', '') else data.get('Art', '')

        # Ersetzt Platzhalter für Inhalt, Stunden und Art in der Zelle.
        self.document.replace_placeholders(cell, placeholder_content, content)
        self.document.replace_placeholders(cell, placeholder_hours, self.CM.get_default_hours())
        self.document.replace_placeholders(cell, placeholder_type, data.get('Art', ''))


    """
    Formatiert den Tätigkeitsinhalt für die Darstellung im Dokument.

    Parameter:
    - content: Der unformatierte Tätigkeitsinhalt.

    Rückgabewert:
    - Ein formatierter String, der für die Darstellung geeignet ist.
    """
    def format_content(self, content: str) -> str:
        content = content.replace('Berufsschule', '').strip()
        return f"-   {content.replace(',', '').replace('- ', '').replace('\n', '\n-   ')}" if content else ''


    """
    Berechnet das Start- und Enddatum einer Woche basierend auf dem Startdatum der CSV-Daten.

    Parameter:
    - start_date: Startdatum als String im Format 'dd.mm.yyyy'.
    - week_offset: Anzahl der Wochen, die vom Startdatum verschoben werden.

    Rückgabewert:
    - Ein Tuple (Startdatum, Enddatum) im Format 'dd.mm.yyyy'.
    """
    def calculate_week_range(self, start_date: str, week_offset: int) -> Tuple[str, str]:
        start = datetime.strptime(start_date, "%d.%m.%Y") + timedelta(weeks=week_offset)
        end = start + timedelta(days=4)  # Angenommen: Woche endet nach 5 Tagen (Montag bis Freitag).
        return start.strftime("%d.%m.%Y"), end.strftime("%d.%m.%Y")

    """
    Verarbeitet alle Wochen und füllt Platzhalter in der Vorlage für jede Woche aus.
    """
    def process_all_weeks(self):
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week, entries)
