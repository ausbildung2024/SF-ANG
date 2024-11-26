import os
from pathlib import Path
APP_NAME = 'SF-ANG'

APPDATA_PATH = Path(os.getenv('APPDATA', ''))  # Der Pfad des APPDATA-Ordners für systemweite Anwendungsdaten

days = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG"]  # Liste der Arbeitstage

activitys = {
    'NE-NICHT-PRÄMIENWIRKSAME AUSBILDUNG': 'Betrieb',  # Aktivitätstypen
    'AS-KRANKHEIT': 'Krank',
    'AH-URLAUB': 'Urlaub',
    'NA': 'TAETIGKEIT_UNBEKANNT'
}

missing_day = {
    'Art': 'Feiertag',  # Standardtyp für fehlende Tage
    'Inhalt': ''  # Details zu fehlenden Tagen
}

messages = {  # Fehler- und Erfolgsmeldungen
    'errors': {
        'file_not_found': "Die Datei '{file}' wurde nicht gefunden.",
        'empty_data': "Die Datei '{file}' ist leer.",
        'missing_columns': "Die CSV-Datei fehlt die folgenden Spalten: {columns}",
        'generic_error': "Ein Fehler ist aufgetreten: {message}",
        'save_error': "Das Dokument konnte nicht gespeichert werden. Fehler: {message}",
        'missing_days': "Tag {day} in Woche {week} ist nicht vorhanden, bitte manuell überprüfen!"
    },
    'success': {
        'file_loaded': "Die Datei '{file}' wurde erfolgreich geladen.",
        'document_saved': "Das Dokument wurde erfolgreich gespeichert unter: {file_path}",
        'config_loaded' : "Einstellungen erfolgreich geladen und aktualisiert."
    },
    'warnings':{

    },
    'infos':{

    }
}

settings = {
    'name': 'Gustav Gustavson',  # Standardbenutzername
    'year': '1',  # Ausbildungsjahr des Nutzers
    'default_hours': '8',  # Standardarbeitsstunden pro Tag
}

app = {
 'name' : APP_NAME,
 'version' : '24.11.26.A'
}

paths = {
    'input_csv': 'data.csv',  # Pfad zur Eingabe-CSV-Datei
    'template': 'src/template/month.docx',  # Pfad zur Dokumentvorlage
    'config' : Path(str(APPDATA_PATH / APP_NAME / 'config.ini')), # Pfad zur Konfig
    'output': 'Ausgabe',  # Ordner für generierte Dokumente
    'output_backup': Path(str(APPDATA_PATH / APP_NAME / 'dokumente')),  # Pfad zum Backup-Ordner
    'log': Path(str(APPDATA_PATH / APP_NAME / 'logs'))  # Pfad zum Log-Ordner
}