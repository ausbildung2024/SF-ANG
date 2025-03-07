"""
Lädt die CSV Datei
"""
from pathlib import Path

import pandas as pd
from numpy.f2py.auxfuncs import throw_error

from src.Settings.ConfigManager import ConfigManager
from src.Utils.DateUtil import *
from src.Utils.FileUtil import is_file_valid

### KONSTANTEN:

#Aktivitäten
ACT_BS = 'Berufsschule'
ACT_BT = 'Betrieb'
ACT_NA = 'NA'
ACT_OT = 'Urlaub/Feiertag'

#CSV FELDER
CSV_ACT = 'Tätigkeitsbeschreibung'
CSV_DAY = 'Tag'
CSV_CON = 'Beschreibung'
CSV_DAT = 'Datum'

#Week Data Datentsätze
WDA_CON = 'Inhalt'
WDA_TYP = 'Art'

#Anderes
DELIMITER = ';' #Wird zum Aufteilen der CSV Datei verwendet.
CSV_FILETYPE = '.csv'

#Error Nachrichten
ERR_CSV_NC = "Das erstellen eines CSV Loaders ist schiefgelaufen"
ERR_CSV_NL = "Das laden der CSV ist schiefgelaufen"
ERR_CSV_NV = 'Die CSV ist nicht vollständig! Es fehlen Folgende Zeilen: {}. Überprüfe ob die CSV die richtige Sprache hat'

"""

"""
class CSVProcessor:
    def __init__(self, config_manager: ConfigManager, path: Path = None):
        self.config : ConfigManager = config_manager
        self.path : Path = path
        self.dataframe = None

        try:
            if path is not None:
                self.load_csv(path)
        except Exception as e:
            e.add_note(ERR_CSV_NC)
            raise e

    """
    Überprüft ob der Pfad Existiert, und wenn lädt er die csv Datei
    
    Attribute:
        path: Der Pfad zu der CSV Datei
    """
    def load_csv(self, path: Path):
        try:
            is_file_valid(path)
            self.path = path
            self.dataframe = pd.read_csv(self.path, delimiter=DELIMITER)
            self.is_csv_valid()
            return True
        except Exception as e:
            raise e

    """
    Überprüft ob die CSV Datei gültig ist.
    """
    def is_csv_valid(self):
        if self.dataframe is None:
            raise Exception(ERR_CSV_NL)

        required_columns = self.config.get_csv_columns()
        missing_columns = required_columns - set(self.dataframe.columns)

        if missing_columns:
            raise Exception(ERR_CSV_NV.format(missing_columns))

    """
    Gibt den Dataframe (CSV) zurück
    """
    def get_dataframe(self):
        return self.dataframe

    def get_start_date(self):
        return get_week_from_date(self.dataframe[CSV_DAT].iloc[0])

    def get_row_entry(self, row):
        return {
            row[CSV_DAY].upper(): {
                WDA_TYP: self.get_activity_type(row[CSV_ACT].upper()),
                WDA_CON: row.get(CSV_CON, ''),
            }
        }

    """
    Wandelt den Tätigkeitswert aus der CSV in den für den nachweis Verwendbaren wert um.

    Attribute:
        activity: die art der Aktivität als string
    """

    def get_activity_type(self, activity: str) -> str:
        return self.config.get_activitys().get(activity, self.config.get_activitys()[ACT_NA])

    """
    Erstellt ein Dictionary für Vorlagen welches für die weitere verarbeitung der Wochendaten benötigt wird. 
    
    Attribute:
            weeks_data: Dictionary, indem die Daten für die Wochen gespeichert werden
            current_week: Integer, welcher die aktuelle Woche darstellt 1-5
            current_day: Integer, welcher den aktuellen Tag darstellt 1-5
            current_day_as_str: String, welcher den aktuellen Tag als String darstellt
    
    Übergabe-Attribute:
        school: Dictionary, indem gespeichert wird an welchen Tagen Berufsschule ist
    """
    def parse_empty_week_data(self, school):
        #Erstellt ein Leerens Week Data Dictionary für 5 Wochen
        weeks_data = {1: [], 2: [], 3: [], 4: [], 5: []}
        #Geht durch jeden Monat und jeden Tag
        for current_week in range(1, 6):
            for current_day in range(0, 5):
                current_day_as_str = self.config.get_work_days()[current_day]
                #Überprüft, ob an dem Tag Schule oder Betrieb ist
                activity = ACT_BS if school[current_day_as_str] else ACT_BT
                #Fügt den Tag zu den wochen hinzu
                weeks_data[current_week].append({current_day_as_str: {WDA_TYP: activity, WDA_CON: ''}})
        return weeks_data

    """
    
    """
    def parse_week_data(self):
        try:
            is_file_valid(self.path,CSV_FILETYPE)
        except Exception as e:
            raise e

        week_data = {}
        start_week = self.get_start_date()

        #Generiert das Week data dictionary
        for _, row in self.dataframe.iterrows():
            #Berechnet die Aktuelle woche für die weitere verarbeitung
            relative_week = get_relative_week(start_week,get_week_from_date(row[CSV_DAT]))
            #Fügt das template mit der Tätigkeit den wochen hinzu
            week_data.setdefault(relative_week, []).append(self.get_row_entry(row))

        #Fügt die Leeren Tage hinzu
        for week, entries in week_data.items():
            existing_days = {tag for entry in entries for tag in entry.keys()}
            missing_days = set(self.config.get_work_days()) - existing_days
            for day in missing_days:
                entries.append({day: {WDA_TYP: ACT_OT, WDA_CON: ""}})
                #Missing Days

        return week_data