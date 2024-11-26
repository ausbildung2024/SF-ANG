import configparser
import logging
import os
from pathlib import Path
from typing import Any, Dict, TypedDict

# Anwendungskonstanten
APP_NAME = 'SF-ANG'
APP_VERSION = '24.11.26.A'
APPDATA_PATH = Path(os.getenv('APPDATA', ''))  # Der Pfad des APPDATA-Ordners für systemweite Anwendungsdaten
CONFIG_PATH = APPDATA_PATH / APP_NAME / 'config.ini'  # Pfad zur Konfigurationsdatei
OUTPUT_BACKUP_PATH = APPDATA_PATH / APP_NAME / 'dokumente'  # Pfad zum Ordner für Backup-Dokumente
LOG_FOLDER_PATH = APPDATA_PATH / APP_NAME / 'logs'  # Pfad zum Ordner für Logs
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
    }
}
settings = {
    'name': 'Gustav Gustavson',  # Standardbenutzername
    'year': '1',  # Ausbildungsjahr des Nutzers
    'default_hours': '8',  # Standardarbeitsstunden pro Tag
    'input_csv': 'data.csv',  # Pfad zur Eingabe-CSV-Datei
    'template': 'src/template/month.docx',  # Pfad zur Dokumentvorlage
    'output_folder': 'Ausgabe',  # Ordner für generierte Dokumente
    'output_backup': Path(str(OUTPUT_BACKUP_PATH)),  # Pfad zum Backup-Ordner
    'log_folder': Path(str(LOG_FOLDER_PATH))  # Pfad zum Log-Ordner
}


class SettingsDict(TypedDict):
    name: str
    year: int
    default_hours: int


# Einrichtung der Protokollierung
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(APP_NAME)


class ConfigManager:
    """Verwaltet das Laden und Speichern der Konfigurationsdatei."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._ensure_path_exists(self.config_path.parent)  # Sicherstellen, dass der Pfad existiert
        self._initialize_config()

    def _initialize_config(self):
        """Lädt oder erstellt die Konfigurationsdatei, wenn sie noch nicht existiert."""
        if not self.config_path.exists():
            logger.info("Konfigurationsdatei existiert nicht. Standardwerte werden erstellt.")
            self._write_defaults()
        else:
            try:
                self.config.read(self.config_path)
                logger.info(f"Konfigurationsdatei erfolgreich geladen: {self.config.sections()}")
            except Exception as e:
                logger.error(f"Fehler beim Laden der Konfigurationsdatei: {e}")
                raise

    def _write_defaults(self):
        """Schreibt nur die relevanten Standardwerte in die Konfigurationsdatei."""
        logger.info("Schreibe Standardwerte in die Konfigurationsdatei.")
        self.config.read_dict({'Settings': {  # Nur relevante Werte speichern
            'name': settings['name'],
            'year': settings['year'],
            'default_hours': settings['default_hours']
        }})
        try:
            with open(self.config_path, 'w') as file:
                self.config.write(file)
            logger.info(f"Konfigurationsdatei erfolgreich erstellt: {self.config_path}")
        except Exception as e:
            logger.error(f"Fehler beim Schreiben der Konfigurationsdatei: {e}")
            raise

    @staticmethod
    def _ensure_path_exists(path: Path):
        """Erstellt den Verzeichnisbaum, falls er nicht existiert."""
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Pfad erstellt: {path}")
            except Exception as e:
                logger.error(f"Fehler beim Erstellen des Pfads {path}: {e}")
                raise

    def get_config_value(self, section: str, key: str, default: Any, value_type: type = str) -> Any:
        """Gibt einen Konfigurationswert aus einem Abschnitt zurück und konvertiert ihn zum gewünschten Typ."""
        try:
            if value_type is int:
                return self.config[section].getint(key, default)
            return self.config[section].get(key, default)
        except (ValueError, KeyError, configparser.NoSectionError, configparser.NoOptionError) as e:
            logger.warning(f"Konfigurationswert '{key}' in Sektion '{section}' fehlt. Fehler: {e}. Verwende Standard: {default}")
            return default

    def load_settings(self, settings_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Lädt nur die gewünschten Werte (`name`, `year`, `default_hours`) in das Settings-Dictionary."""
        settings_dict['name'] = self.get_config_value('Settings', 'name', settings_dict.get('name', settings['name']))
        settings_dict['year'] = self.get_config_value('Settings', 'year', settings_dict.get('year', int(settings['year'])), int)
        settings_dict['default_hours'] = self.get_config_value('Settings', 'default_hours', settings_dict.get('default_hours', int(settings['default_hours'])), int)
        logger.info(messages['success']['config_loaded'])
        return settings_dict


# Instanziierung und Nutzung des Konfigurationsmanagers
logger.info("Start der Anwendung.")
config_manager = ConfigManager(CONFIG_PATH)

# Das bestehende Settings-Dict wird ergänzt
settings = config_manager.load_settings(settings)  # Nur ausgewählte Werte werden überschrieben
