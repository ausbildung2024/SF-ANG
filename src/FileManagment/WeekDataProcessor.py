from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd

from src.FileManagment.CSVProcessor import CSVProcessor
from src.Settings.ConfigManager import ConfigManager
from src.FileManagment.WordProcessor import WordTemplate
from src.Utils.DateUtil import get_week_range


class WeekDataProcessor:
    """
    Verarbeitet Wochendaten aus einer CSV und füllt Platzhalter in einer Word-Vorlage.
    """

    def __init__(self, CM: ConfigManager, document: WordTemplate, csv: CSVProcessor = None):
        self.CM = CM
        self.document = document
        self.csv_processor = csv
        self.csv = None
        if csv is not None:
            self.csv = csv.get_dataframe()

        self.weeks_data = self.initialize_weeks_data()

    def initialize_weeks_data(self):
        if self.csv is None:
            return self.csv_processor.parse_empty_week_data()
        else:
            return self.csv_processor.parse_week_data()

    def process_week_placeholders(self, week, entries, date = None):
        """Ersetzt Platzhalter für eine Woche im Dokument."""
        if self.csv is None:
            start_date, end_date = get_week_range(date, week -1)
        else:
            start_date, end_date = get_week_range(self.csv['Datum'][0], week - 1)

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

    def process_all_weeks(self):
        """Füllt Platzhalter für alle Wochen aus."""
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week, entries)

    def process_all_empty_weeks(self, date):
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week,entries,f"1.{date['month']}.{date['year']}")