import os
from pathlib import Path

APP_NAME = 'SF-ANG'
APP_VERSION = '08.01.25.A3'

APPDATA_PATH = Path(os.getenv('APPDATA', ''))  # Der Pfad des APPDATA-Ordners für systemweite Anwendungsdaten

settings = {
    'work_days': ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG"],  # Liste der Arbeitstage
    'csv_columns' : {'Datum', 'Tag', 'Tätigkeitsbeschreibung', 'Beschreibung'},
    'activitys': {
        'NE-NICHT-PRÄMIENWIRKSAME AUSBILDUNG': 'Betrieb',  # Aktivitätstypen
        'AS-KRANKHEIT': 'Krank',
        'AH-URLAUB': 'Urlaub',
        'NA': 'Tätigkeit unbekannt! '
    },

    'missing_day': {
        'Art': 'Feiertag',  # Standardtyp für fehlende Tage
        'Inhalt': ''  # Details zu fehlenden Tagen
    },

    'messages': {  # Fehler- und Erfolgsmeldungen
        'errors': {
            'file_not_found': "Die Datei '{file}' wurde nicht gefunden.",
            'empty_data': "Die Datei '{file}' ist leer.",
            'missing_columns': "Die CSV-Datei fehlt die folgenden Spalten: {columns}",
            'generic_error': "Ein Fehler ist aufgetreten: {message}",
            'save_error': "Das Dokument konnte nicht gespeichert werden. Fehler: {message}",
            'missing_days': "Tag {day} in Woche {week} ist nicht vorhanden, bitte manuell überprüfen!",
            'laden_vorlage': "Fehler beim laden der Vorlage",
        },
        'success': {
            'file_loaded': "Die Datei '{file}' wurde erfolgreich geladen.",
            'document_saved': "Das Dokument wurde erfolgreich gespeichert unter: {file_path}",
            'config_loaded': "Einstellungen erfolgreich geladen und aktualisiert.",
        },
        'warnings': {

        },
        'infos': {

        }
    },

    'personal': {
        'name': 'Gustav Gustavson',  # Standardbenutzername
        'year': '1',  # Ausbildungsjahr des Nutzers
        'default_hours': '8',  # Standardarbeitsstunden pro Tag
    },

    'app': {
        'name': APP_NAME,
        'version': APP_VERSION,
        'id' : 'ausbildung2024.' + APP_NAME + 'V' +  APP_VERSION
    },

    'paths': {
        'input_csv': Path.home() / 'Downloads',  # Pfad zur Eingabe-CSV-Datei
        'template': Path.cwd() / 'res/template/month.docx',  # Pfad zur Dokumentvorlage
        'config': Path(str(APPDATA_PATH / APP_NAME / 'config.ini')),  # Pfad zur Konfig
        'output':  Path.home() / 'Documents',  # Ordner für generierte Dokumente
        'output_backup': Path(str(APPDATA_PATH / APP_NAME / 'dokumente')),  # Pfad zum Backup-Ordner
        'log': Path(str(APPDATA_PATH / APP_NAME / 'logs')),  # Pfad zum Log-Ordner
        'icon_large': Path.cwd() / 'res/pictures/icon_16x.png',
        'icon_small': Path.cwd() / 'res/pictures/icon_32x.png',
    },

    'labels': {
        'name': 'Name',
        'year' : 'Ausbildungsjahr:',
        'hour' : 'Standard Stunden',
        'csv' : 'Pfad CSV:',
        'template' : 'Pfad Vorlage:',
        'output' : 'Ausgabe Ordner:',
        'generate' : 'Generieren',
        'select' : 'Auswahl',
        'erfolg' : 'Erfolgreich',
        'fehler' : 'Fehler'
    },

    'filetypes':{
        'csv': [("CSV-Dateien", "*.csv")],
        'word':[("Word-Dokumente", "*.docx")]
    },
    'links':{
        'time_portal': 'https://portal.nagarro-es.com/ess/shells/abap/FioriLaunchpad.html#TIMEREPORTING_NAG-create?OnBehalfOf'
    }
}
