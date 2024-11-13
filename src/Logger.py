import logging
from datetime import datetime
from pathlib import Path


class Logger:
    """Konfiguriert und initialisiert das Logging für die Anwendung."""

    def __init__(self, log_folder: Path):
        """
        Initialisiert die Logger-Klasse und erstellt ein Logfile im angegebenen Verzeichnis.

        Parameter:
        - log_folder: Der Ordnerpfad, in dem die Logdateien gespeichert werden.
        """
        # Erstellt das Verzeichnis für die Logdateien, falls es nicht existiert.
        log_folder.mkdir(parents=True, exist_ok=True)

        # Generiert den Dateinamen für die Logdatei mit aktuellem Datum und Uhrzeit.
        log_file = log_folder / f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

        # Konfiguriert die Grundeinstellungen für das Logging.
        logging.basicConfig(
            level=logging.INFO,  # Standard-Log-Level auf INFO setzen.
            format='%(asctime)s - %(levelname)s - %(message)s',  # Log-Ausgabeformat: Zeitstempel, Level, Nachricht.
            handlers=[
                logging.StreamHandler(),  # Ausgabe der Lognachrichten in die Konsole.
                logging.FileHandler(log_file)  # Speicherung der Lognachrichten in der Logdatei.
            ]
        )

        # Erstellt einen Logger für die Klasse, der mit der obigen Konfiguration arbeitet.
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        """
        Gibt das konfigurierte Logger-Objekt zurück.

        Rückgabewert:
        - Ein Logger-Objekt, das für Logging-Aufgaben verwendet werden kann.
        """
        return self.logger
