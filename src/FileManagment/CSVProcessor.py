from src.Utils.CONSTANTS import *

"""
Der CSV Processor Lädt eine Nachweis-CSV Und überprüft diese auf die richtige Formatierung.

Parameter:
    config_manager: ConfigManager instanz zum laden der Einstellungen
    path: Pfad zur CSV Datei
"""
class CSVProcessor:
    def __init__(self, path: Path = None):
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
            self.dataframe = pd.read_csv(self.path, delimiter=CSV_DIL)
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

        required_columns = CSV_FLDS
        missing_columns = required_columns - set(self.dataframe.columns)

        if missing_columns:
            raise Exception(ERR_CSV_NV.format(missing_columns))

    """
    Gibt den Dataframe (CSV) zurück
    """
    def get_dataframe(self):
        return self.dataframe

    """
    Holt sich das Datum aus der CSV
    """
    def get_start_date(self):
        return get_week_from_date(self.dataframe[CSV_FLD_DAT].iloc[0])

    """
    Generiert Daten aus der CSV
    
    Attribute:
        row: Die Daten, welche in die Entry geladen werden
    """
    def get_row_entry(self, row):
        return {
            row[CSV_FLD_DAY].upper(): {
                WDA_TYP: self.get_activity_type(row[CSV_FLD_ACT].upper()),
                WDA_CON: row.get(CSV_FLD_CON, ''),
            }
        }

    """
    Wandelt den Tätigkeitswert aus der CSV in den für den nachweis Verwendbaren wert um.

    Attribute:
        activity: die art der Aktivität als string
    """
    def get_activity_type(self, activity: str) -> str:
        if activity in CSV_ACTIVITY:
            return  CSV_ACTIVITY[activity]
        else:
            return  CSV_ACTIVITY['NA']

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
                current_day_as_str = WORK_DAYS[current_day]
                #Überprüft, ob an dem Tag Schule oder Betrieb ist
                activity = ACT_BS if school[current_day_as_str] else ACT_BT
                #Fügt den Tag zu den wochen hinzu
                weeks_data[current_week].append({current_day_as_str: {WDA_TYP: activity, WDA_CON: ''}})
        return weeks_data

    """
    Erstellt ein Dictionary für aus den Daten der CSV, welches für die weitere verarbeitung der Wochentage benötigt wird. 
    """
    def parse_week_data(self):
        try:
            is_file_valid(self.path,FILETYPE_CSV)
        except Exception as e:
            raise e

        week_data = {}
        start_week = self.get_start_date()

        #Generiert das Week data dictionary
        for _, row in self.dataframe.iterrows():
            #Berechnet die Aktuelle woche für die weitere verarbeitung
            relative_week = get_relative_week(start_week,get_week_from_date(row[CSV_FLD_DAT]))
            #Fügt das template mit der Tätigkeit den wochen hinzu
            week_data.setdefault(relative_week, []).append(self.get_row_entry(row))

        #Fügt die Leeren Tage hinzu
        for week, entries in week_data.items():
            existing_days = {tag for entry in entries for tag in entry.keys()}
            missing_days = set(WORK_DAYS) - existing_days
            for day in missing_days:
                entries.append({day: {WDA_TYP: ACT_OT, WDA_CON: ""}})

        return week_data