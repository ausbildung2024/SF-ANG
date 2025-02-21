import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.Settings.ConfigManager import ConfigManager

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