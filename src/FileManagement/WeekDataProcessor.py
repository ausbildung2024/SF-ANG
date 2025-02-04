from datetime import datetime, timedelta, date
from locale import currency
from typing import Tuple

import pandas as pd

from src.SettingManagement.ConfigManager import ConfigManager
from src.FileManagement.WordTemplate import WordTemplate


class WeekDataProcessor:
    """
    Verarbeitet Wochendaten aus einer CSV und füllt Platzhalter in einer Word-Vorlage.
    """

    def __init__(self, CM: ConfigManager, document: WordTemplate, csv: pd.DataFrame = None):
        self.logger = CM.get_logger()
        self.CM = CM
        self.document = document
        self.csv = csv
        self.weeks_data = self.initialize_weeks_data()

    def get_week(self, date_str: str) -> int:
        """Berechnet die Kalenderwoche aus einem Datum."""
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").isocalendar()[1]
        except ValueError as e:
            self.logger.error(f"Fehler beim Parsen des Datums '{date_str}': {e}")
            return -1

    def get_activity_type(self, activity: str) -> str:
        """Gibt den Typ einer Tätigkeit zurück oder einen Standardwert."""
        return self.CM.get_activitys().get(activity, self.CM.get_activitys()['NA'])

    def initialize_week_data_from_csv(self):
        """Organisiert Daten nach Kalenderwochen."""
        weeks_data = {}

        start_week = self.get_week(self.csv['Datum'].iloc[0])

        for _, row in self.csv.iterrows():
            current_week = self.get_week(row['Datum'])
            relative_week = current_week - start_week + 1
            row_entry = {
                row['Tag'].upper(): {
                    "Art": self.get_activity_type(row['Tätigkeitsbeschreibung'].upper()),
                    "Inhalt": row.get('Beschreibung', ''),
                }
            }
            weeks_data.setdefault(relative_week, []).append(row_entry)

        for week, entries in weeks_data.items():
            existing_days = {tag for entry in entries for tag in entry.keys()}
            missing_days = set(self.CM.get_work_days()) - existing_days
            for day in missing_days:
                entries.append({day: {"Art": "", "Inhalt": ""}})
                self.logger.warning(self.CM.get_error_messages()['missing_days'].format(day=day, week=week))

        return weeks_data

    def initialize_week_data_empty(self):
        weeks_data = {1:[],2:[],3:[],4:[],5:[]}
        for current_week in range(1,6): # 5Tage 5 Wochen
            for current_day in range(0,5):
                weeks_data[current_week].append({self.CM.get_work_days()[current_day]:{'Art':'Betrieb','Inhalt':''}})
        return weeks_data

    def initialize_weeks_data(self):
        if self.csv is None:
            return self.initialize_week_data_empty()
        else:
            return self.initialize_week_data_from_csv()




    def process_week_placeholders(self, week, entries, date = None):
        """Ersetzt Platzhalter für eine Woche im Dokument."""
        if self.csv is None:
            start_date, end_date = self.calculate_week_range(date, week -1)
        else:
            start_date, end_date = self.calculate_week_range(self.csv['Datum'][0], week - 1)

        general_placeholders = {
            '{NAME}': self.CM.get_name(),
            '{ABJ}': self.CM.get_year(),
            f'{{DATUM_START{week}}}': start_date,
            f'{{DATUM_ENDE{week}}}': end_date
        }

        for table in self.document.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.document.replace_general_placeholders(cell, general_placeholders)
                    for day in self.CM.get_work_days():
                        day_data = next((entry.get(day, {}) for entry in entries if day in entry), {})
                        self.replace_placeholders_for_day(cell, day, week, day_data)

    def replace_placeholders_for_day(self, cell, day, week, data):
        """Ersetzt Platzhalter für einen bestimmten Tag."""
        placeholders = {
            f"{{{day}_INHALT{week}}}": self.format_content(data.get('Inhalt', '')),
            f"{{{day}_STUNDEN{week}}}": self.CM.get_default_hours(),
            f"{{{day}_ART{week}}}": 'Berufsschule' if 'Berufsschule' in data.get('Inhalt', '') else data.get('Art', '')
        }
        for placeholder, value in placeholders.items():
            self.document.replace_placeholders(cell, placeholder, value)

    def format_content(self, content: str) -> str:
        """Formatiert Tätigkeitsinhalt für das Dokument."""
        content = content.replace('Berufsschule', '').strip()
        return f"-   {content.replace(',', '').replace('- ', '').replace('\n', '\n-   ')}" if content else ''

    def calculate_week_range(self, start_date: str, week_offset: int) -> Tuple[str, str]:
        """Berechnet Start- und Enddatum einer Woche."""
        start = datetime.strptime(start_date, "%d.%m.%Y")
        days_to_monday = (start.weekday() - 0) % 7
        start_of_week = start - timedelta(days=days_to_monday) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=(4 - start_of_week.weekday()) % 7)
        return start_of_week.strftime("%d.%m.%Y"), end_of_week.strftime("%d.%m.%Y")

    def process_all_weeks(self):
        """Füllt Platzhalter für alle Wochen aus."""
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week, entries)

    def process_all_empty_weeks(self, date):
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week,entries,f"1.{date['month']}.{date['year']}")