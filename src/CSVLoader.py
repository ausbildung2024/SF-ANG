from pathlib import Path
from typing import Optional

import pandas as pd


class CSVLoader:
    """Lädt CSV-Daten und validiert das Format."""

    def __init__(self, logger, file_path: Path):
        """
        Initialisiert den CSVLoader mit einem Logger und dem Pfad zur CSV-Datei.

        Parameter:
        - logger: Ein Logger-Objekt zum Protokollieren von Lade- und Fehlerereignissen.
        - file_path: Der Pfad zur CSV-Datei als Path-Objekt.
        """
        self.logger = logger
        self.file_path = file_path

    def load(self) -> Optional[pd.DataFrame]:
        """
        Lädt die CSV-Datei und validiert das Vorhandensein erforderlicher Spalten.

        Rückgabewert:
        - Gibt ein DataFrame zurück, wenn die Datei erfolgreich geladen und validiert wurde.
        - Gibt None zurück, falls ein Fehler auftritt oder erforderliche Spalten fehlen.
        """
        try:
            # Überprüft, ob die Datei am angegebenen Pfad existiert.
            if not self.file_path.exists():
                self.logger.error(f"Datei nicht gefunden: {self.file_path}")
                return None

            # Lädt die CSV-Datei als DataFrame, erwartet ';' als Trennzeichen.
            df = pd.read_csv(self.file_path, delimiter=';')

            # Definiert die für die weitere Verarbeitung erforderlichen Spaltennamen.
            required_columns = {'Datum', 'Tag', 'Tätigkeitsbeschreibung', 'Beschreibung'}

            # Überprüft, ob alle erforderlichen Spalten vorhanden sind.
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                # Protokolliert die fehlenden Spalten, falls welche fehlen.
                self.logger.error(f"Fehlende Spalten: {', '.join(missing_columns)}")
                return None

            # Protokolliert, dass die Datei erfolgreich geladen wurde.
            self.logger.info(f"Datei erfolgreich geladen: {self.file_path}")
            return df

        except pd.errors.EmptyDataError:
            # Fehlerbehandlung, falls die CSV-Datei leer ist.
            self.logger.error(f"Leere Datei: {self.file_path}")
            return None

        except Exception as e:
            # Allgemeine Fehlerbehandlung für andere Ausnahmen.
            self.logger.error(f"Fehler: {str(e)}")
            return None
