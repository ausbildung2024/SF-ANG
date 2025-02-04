import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.SettingManagement.ConfigManager import ConfigManager

"""
Erstellt einen Logger an dem richtigen Pfad
"""
def create_logger(CM: ConfigManager):
    # Log File erstellen
    log_folder = Path(CM.get_log_path())
    log_folder.mkdir(parents=True, exist_ok=True)  # Erstellt das Log verzeichnis falls nicht vorhanden
    log_file = log_folder / f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'  # Generiert den Dateinamen für die Logdatei mit aktuellem Datum und Uhrzeit.

    # Konfiguriert die Grundeinstellungen für das Logging.
    logging.basicConfig(
        level=logging.INFO,  # Standard-Log-Level auf INFO setzen.
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log-Ausgabeformat: Zeitstempel, Level, Nachricht.
        handlers=[
            logging.StreamHandler(),  # Ausgabe der Lognachrichten in die Konsole.
            logging.FileHandler(log_file)  # Speicherung der Lognachrichten in der Logdatei.
        ]
    )

    return logging.getLogger(__name__)


"""
Lädt die CSV Datei
"""
def load_csv(CM: ConfigManager, logger:logging, path : Path):

    try:

        if not path.exists():
            logger.error(f"Datei nicht gefunden: {path}")
            return None

        df = pd.read_csv(path, delimiter=';') #Liest die csv mit dem Trennzeichen ';'

        required_columns = CM.get_csv_columns()
        missing_columns = required_columns - set(df.columns)  # Überprüft, ob alle erforderlichen Spalten vorhanden sind.

        if missing_columns:
            logger.error(
                f"Fehlende Spalten: {', '.join(missing_columns)}")  # Protokolliert die fehlenden Spalten, falls welche fehlen.
            return None

        logger.info(f"Datei erfolgreich geladen: {path}")
        return df

    except pd.errors.EmptyDataError:  # Fehlerbehandlung, falls die CSV-Datei leer ist.
        logger.error(f"Leere Datei: {path}")
        return None

    except Exception as e:  # Allgemeine Fehlerbehandlung für andere Ausnahmen.
        logger.error(f"Fehler: {str(e)}")
        return None

