"""
Lädt die CSV Datei
"""
from pathlib import Path

import pandas as pd
from src.Settings.ConfigManager import ConfigManager
from src.Utils.DateUtil import *

DELIMITER = ';'

class CSVProcessor:
    def __init__(self, config_manager: ConfigManager, path: Path = None):
        self.config : ConfigManager = config_manager
        self.path : Path = path
        self.dataframe = None

        if path is not None:
            self.load_csv(path)

    def is_path_valid(self, path: Path):
        return path.exists()

    def load_csv(self, path: Path):

        if self.is_path_valid(path):
            self.set_csv_path(path)
            self.dataframe = pd.read_csv(self.path,delimiter=DELIMITER)
            return self.is_csv_valid()
        return 'CSV Pfad nicht gefunden'

    def is_csv_valid(self):
        if self.dataframe is None:
            return 'CSV not loaded'

        required_columns = self.config.get_csv_columns()
        missing_columns = required_columns - set(self.dataframe.columns)

        if missing_columns:
            return f'CSV missing columns: {missing_columns}'

        return True

    def get_dataframe(self):
        return self.dataframe

    def set_csv_path(self, csv_path: Path):
        self.path = csv_path

    def get_config_manager(self):
        return self.config

    def set_config_manager(self, config_manager: ConfigManager):
        self.config = config_manager

    def get_start_date(self):
        return get_week_from_date(self.dataframe['Datum'].iloc[0])

    def get_row_entry(self,row):
        return {
            row['Tag'].upper(): {
                "Art": self.get_activity_type(row['Tätigkeitsbeschreibung'].upper()),
                "Inhalt": row.get('Beschreibung', ''),
            }
        }

    def parse_empty_week_data(self, school):
        weeks_data = {1: [], 2: [], 3: [], 4: [], 5: []}
        for current_week in range(1, 6):  # 5Tage 5 Wochen
            for current_day in range(0, 5):

                weeks_data[current_week].append(
                    {self.config.get_work_days()[current_day]: {'Art': 'Betrieb', 'Inhalt': ''}})
        return weeks_data

    def parse_week_data(self):
        if not self.is_path_valid(self.path):
            return 'Pfad nicht gefunden'

        week_data = {}
        start_week = self.get_start_date()

        #Generiert das Week data dictionary
        for _, row in self.dataframe.iterrows():
            #Berechnet die Aktuelle woche für die weitere verarbeitung
            relative_week = get_relative_week(start_week,get_week_from_date(row['Datum']))
            #Fügt das template mit der Tätigkeit den wochen hinzu
            week_data.setdefault(relative_week, []).append(self.get_row_entry(row))

        #Fügt die Leeren Tage hinzu
        for week, entries in week_data.items():
            existing_days = {tag for entry in entries for tag in entry.keys()}
            missing_days = set(self.config.get_work_days()) - existing_days
            for day in missing_days:
                entries.append({day: {"Art": "Urlaub/Feiertag", "Inhalt": ""}})
                #Missing Days

        return week_data

    def get_activity_type(self, activity: str) -> str:
        """Gibt den Typ einer Tätigkeit zurück oder einen Standardwert."""
        return self.config.get_activitys().get(activity, self.config.get_activitys()['NA'])