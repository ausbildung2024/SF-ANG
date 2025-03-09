from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd

from src.FileManagment.CSVProcessor import CSVProcessor
from src.FileManagment.WordProcessor import WordTemplate
from src.Utils.CONSTANTS import *
from src.Utils.DateUtil import get_week_range


class WeekDataProcessor:
    """
    Verarbeitet Wochendaten aus einer CSV und füllt Platzhalter in einer Word-Vorlage.
    """
    def __init__(self , document: WordTemplate, csv: CSVProcessor = None, school = None):
        self.document = document
        self.csv_processor = csv
        self.csv = None
        if csv is not None:
            self.csv = csv.get_dataframe()

        self.weeks_data = self.initialize_weeks_data(school)

    def initialize_weeks_data(self,school = None):
        try:
            if self.csv is None:
                return self.csv_processor.parse_empty_week_data(school)
            else:
                return self.csv_processor.parse_week_data()
        except Exception as e:
            raise e

    def process_week_placeholders(self, week, entries, data, date = None):
        """Ersetzt Platzhalter für eine Woche im Dokument."""
        if self.csv is None:
            start_date, end_date = get_week_range(date, week -1)
        else:
            start_date, end_date = get_week_range(self.csv[CSV_FLD_DAT][0], week - 1)

        general_placeholders = {
            '{NAME}': data['name'],
            '{ABJ}': data['year'],
            f'{{DATUM_START{week}}}': start_date,
            f'{{DATUM_ENDE{week}}}': end_date
        }

        for table in self.document.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.document.replace_general_placeholders(cell, general_placeholders)
                    for day in WORK_DAYS:
                        day_data = next((entry.get(day, {}) for entry in entries if day in entry), {})
                        self.replace_placeholders_for_day(cell, day, week, day_data)

    def replace_placeholders_for_day(self, cell, day, week, data):
        """Ersetzt Platzhalter für einen bestimmten Tag."""
        placeholders = {
            f"{{{day}_INHALT{week}}}": self.format_content(data.get(WDA_CON, '')),
            f"{{{day}_STUNDEN{week}}}": WORK_HOURS,
            f"{{{day}_ART{week}}}": ACT_BS if ACT_BS in data.get(WDA_CON, '') else data.get(WDA_TYP, '')
        }
        for placeholder, value in placeholders.items():
            self.document.replace_placeholders(cell, placeholder, value)

    def format_content(self, content: str) -> str:
        """Formatiert Tätigkeitsinhalt für das Dokument."""
        content = content.replace(ACT_BS, '').strip()
        #Schwarze Magie
        return f"-   {content.replace(',', '').replace('- ', '').replace('\n', '\n-   ')}" if content else ''

    def process_all_weeks(self,data):
        """Füllt Platzhalter für alle Wochen aus."""
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week, entries, data)

    def process_all_empty_weeks(self, date, data,  schooldays):
        for week, entries in self.weeks_data.items():
            self.process_week_placeholders(week,entries,data,f"1.{date['month']}.{date['year']}")