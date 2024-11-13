import configparser
import logging
import os
from pathlib import Path
from typing import Any, Dict, TypedDict

# Anwendungskonstanten
APP_NAME = 'auto-nachweise'
APPDATA_PATH = Path(os.getenv('APPDATA', ''))  # Der Pfad des APPDATA-Ordners für systemweite Anwendungsdaten
CONFIG_PATH = APPDATA_PATH / APP_NAME / 'config.ini'  # Pfad zur Konfigurationsdatei
OUTPUT_BACKUP_PATH = APPDATA_PATH / APP_NAME / 'dokumente'  # Pfad zum Ordner für Backup-Dokumente
LOG_FOLDER_PATH = APPDATA_PATH / APP_NAME / 'logs'  # Pfad zum Ordner für Logs
days = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG"]  # Liste der Arbeitstage

# Standardwerte für die Konfiguration
DEFAULTS = {
    'Settings': {
        'name': 'Max Wiegel',  # Standardbenutzername
        'year': '1',  # Ausbildungsjahr des Nutzers
        'default_hours': '8',  # Standardarbeitsstunden pro Tag
        'input_csv': 'Vorlagen/data.csv',  # Pfad zur Eingabe-CSV-Datei
        'template': 'Vorlagen/VorlageMonat.docx',  # Pfad zur Dokumentvorlage
        'output_folder': 'Ausgabe',  # Ordner für generierte Dokumente
        'output_backup': str(OUTPUT_BACKUP_PATH),  # Pfad zum Backup-Ordner
        'log_folder': str(LOG_FOLDER_PATH)  # Pfad zum Log-Ordner
    },
    'Activitys': {
        'NE-NICHT-PRÄMIENWIRKSAME AUSBILDUNG': 'Betrieb',  # Aktivitätstypen
        'AS-KRANKHEIT': 'Krank',
        'AH-URLAUB': 'Urlaub',
        'NA': 'TAETIGKEIT_UNBEKANNT'
    },
    'MissingDay': {
        'Art': 'Feiertag',  # Standardtyp für fehlende Tage
        'Inhalt': ''  # Details zu fehlenden Tagen
    },
    'Messages.Errors': {  # Fehlernachrichten
        'file_not_found': "Die Datei '{file}' wurde nicht gefunden.",
        'empty_data': "Die Datei '{file}' ist leer.",
        'missing_columns': "Die CSV-Datei fehlt die folgenden Spalten: {columns}",
        'generic_error': "Ein Fehler ist aufgetreten: {message}",
        'save_error': "Das Dokument konnte nicht gespeichert werden. Fehler: {message}",
        'missing_days': "Tag {day} in Woche {week} ist nicht vorhanden, bitte manuell überprüfen!"
    },
    'Messages.Success': {  # Erfolgsnachrichten
        'file_loaded': "Die Datei '{file}' wurde erfolgreich geladen.",
        'document_saved': "Das Dokument wurde erfolgreich gespeichert unter: {file_path}"
    }
}


# Definition spezifischer Typen für die Konfigurationsabschnitte
class SettingsDict(TypedDict):
    name: str
    year: int
    default_hours: int
    input_csv: Path
    template: Path
    output_folder: Path
    output_backup: Path
    log_folder: Path


class MessagesDict(TypedDict):
    errors: Dict[str, str]
    success: Dict[str, str]


# Einrichtung der Protokollierung
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(APP_NAME)


class BaseConfigManager:
    """Basis-Konfigurationsmanager zur Verwaltung der Konfigurationsdatei."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._initialize_config()

    def _initialize_config(self):
        """Lädt oder erstellt die Konfigurationsdatei, wenn sie noch nicht existiert."""
        if not self.config_path.exists():
            self._write_defaults()
            logger.info(f"{self.config_path} wurde mit Standardwerten erstellt.")
        else:
            self.config.read(self.config_path)
            self._update_all_sections_with_defaults()

    def _write_defaults(self):
        """Schreibt die Standardkonfiguration in die Konfigurationsdatei."""
        for section, defaults in DEFAULTS.items():
            self.config[section] = defaults
        self._ensure_path_exists(self.config_path.parent)
        with open(self.config_path, 'w') as file:
            self.config.write(file)

    def _update_all_sections_with_defaults(self):
        """Aktualisiert alle Abschnitte mit Standardwerten, falls Schlüssel fehlen."""
        updated = False
        for section, defaults in DEFAULTS.items():
            if self.update_section_with_defaults(section, defaults):
                updated = True
        if updated:
            with open(self.config_path, 'w') as file:
                self.config.write(file)
            logger.info(f"{self.config_path} wurde aktualisiert.")

    def update_section_with_defaults(self, section: str, defaults: Dict[str, Any]) -> bool:
        """Aktualisiert einen Abschnitt mit Standardwerten, falls Schlüssel fehlen."""
        section_updated = False
        if section not in self.config:
            self.config[section] = defaults
            section_updated = True
        else:
            for key, value in defaults.items():
                if key not in self.config[section]:
                    self.config[section][key] = str(value)
                    section_updated = True
        return section_updated

    def _ensure_path_exists(self, path: Path):
        """Erstellt den Verzeichnisbaum, falls er nicht existiert."""
        path.mkdir(parents=True, exist_ok=True)

    def get_config_value(self, section: str, key: str, default: Any, value_type: type = str) -> Any:
        """Gibt einen Konfigurationswert aus einem Abschnitt zurück und konvertiert ihn zum gewünschten Typ."""
        try:
            if value_type is int:
                return self.config[section].getint(key, default)
            elif value_type is float:
                return self.config[section].getfloat(key, default)
            elif value_type is bool:
                return self.config[section].getboolean(key, default)
            else:
                return self.config[section].get(key, default)
        except (ValueError, KeyError, configparser.NoSectionError, configparser.NoOptionError):
            return default


class ConfigManager(BaseConfigManager):
    """Erweiterter Konfigurationsmanager für die spezifischen Anforderungen von auto-nachweise."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        super().__init__(config_path)
        self._cache = {}

    def _get_cached_value(self, section: str, key: str, default: Any, value_type: type = str) -> Any:
        """Liest einen Konfigurationswert aus dem Cache oder speichert ihn nach dem ersten Abruf."""
        if (section, key) not in self._cache:
            self._cache[(section, key)] = self.get_config_value(section, key, default, value_type)
        return self._cache[(section, key)]

    @property
    def settings(self) -> SettingsDict:
        """Gibt die Benutzereinstellungen als getyptes Dictionary zurück."""
        settings = DEFAULTS['Settings']
        return {
            'name': self._get_cached_value('Settings', 'name', settings['name']),
            'year': self._get_cached_value('Settings', 'year', int(settings['year']), int),
            'default_hours': self._get_cached_value('Settings', 'default_hours', int(settings['default_hours']), int),
            'input_csv': Path(self._get_cached_value('Settings', 'input_csv', settings['input_csv'])),
            'template': Path(self._get_cached_value('Settings', 'template', settings['template'])),
            'output_folder': Path(self._get_cached_value('Settings', 'output_folder', settings['output_folder'])),
            'output_backup': Path(self._get_cached_value('Settings', 'output_backup', settings['output_backup'])),
            'log_folder': Path(self._get_cached_value('Settings', 'log_folder', settings['log_folder']))
        }

    @property
    def activitys(self) -> Dict[str, str]:
        """Gibt das Aktivitäten-Wörterbuch zurück, wobei die Werte kapitalisiert sind."""
        return {key.upper(): value.capitalize() for key, value in self.config['Activitys'].items()}

    @property
    def missing_day(self) -> Dict[str, str]:
        """Gibt die Standardkonfiguration für fehlende Tage zurück."""
        return dict(self.config['MissingDay'])

    @property
    def messages(self) -> MessagesDict:
        """Gibt die Konfigurationsnachrichten für Fehler und Erfolge zurück."""
        return {
            'errors': dict(self.config['Messages.Errors']),
            'success': dict(self.config['Messages.Success'])
        }


# Instanziierung und Nutzung des Konfigurationsmanagers
config_manager = ConfigManager()

settings = config_manager.settings
missing_day = config_manager.missing_day
messages = config_manager.messages
activitys = config_manager.activitys
