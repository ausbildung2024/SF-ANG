"""
Lädt die CSV Datei
"""
from pathlib import Path

import pandas as pd
from src.Settings.ConfigManager import ConfigManager

def load_csv(CM: ConfigManager, path : Path):
    logger = CM.get_logger()

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