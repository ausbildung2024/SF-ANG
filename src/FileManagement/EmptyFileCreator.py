from datetime import datetime
from typing import Dict
from docx import Document  # python-docx wird benötigt
from src.SettingManagement.SettingsHandler import ConfigManager
from src.FileManagement.WordTemplate import WordTemplate


class EmptyFileCreator:
    """
    Entfernt alle Platzhalter aus einem Word-Dokument und fügt nur das Datum (Jahr und Monat) ein.
    """

    def __init__(self, logger, CM: ConfigManager, document: WordTemplate, datum: Dict[str, int]):
        self.site = 0
        self.logger = logger
        self.CM = CM
        self.document = document.document  # Das Dokumentobjekt wird direkt verarbeitet
        self.datum = datum

    def clear_placeholders(self):
        """
        Entfernt alle Platzhalter aus dem Dokument und fügt nur das Datum ein.
        """
        year = self.datum.get('year', '')
        month = self.datum.get('month', '')

        # Validierung des Datums
        if not isinstance(year, int) or not isinstance(month, int):
            self.logger.error("Ungültiges Datum: 'year' und 'month' müssen Ganzzahlen sein.")
            return

        try:
            # Monat als lesbaren Namen formatieren
            month_name = datetime(year, month, 1).strftime("%B")
        except ValueError as e:
            self.logger.error(f"Fehler beim Verarbeiten des Datums: {e}")
            return

        formatted_date = f"{month_name} {year}"

        # Iteriere über alle Tabellen im Dokument
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    original_text = cell.text
                    if original_text == "Nagarro ES GmBh":
                        self.site += 1
                    updated_text = self._replace_placeholder(original_text, formatted_date)
                    updated_text = self._replace_unused_placeholder(updated_text)
                    cell.text = updated_text

        self.logger.info("Platzhalter wurden entfernt und Datum eingefügt.")


    ""
    @staticmethod
    def _replace_placeholder(text: str, formatted_date: str) -> str:
        import re
        # Suche nach spezifischen Platzhaltern und ersetze sie durch das Datum
        text = re.sub(r"\{DATUM_START\d+}", formatted_date, text)
        text = re.sub(r"\{DATUM_ENDE\d+}", formatted_date, text)
        # Suche nach Namen Platzhalter und ersetze sie durch den Namen
        text = re.sub(r"\{NAME}","Test",text)
        # Suche nach Abschlussjahr Platzhalter und ersetze sie durch den Namen
        text = re.sub(r"\{ABJ}", "1", text)
        # Suche nach Stunden Platzhalter und ersetze sie durch den Namen
        text = re.sub(r"{[A-Z]*_STUNDEN\d+}","8",text)
        return text

    """
    Entfernt alle unbenutzten Platzhalter aus dem Text.
    """
    @staticmethod
    def _replace_unused_placeholder(text: str) -> str:
        import re
        return re.sub(r"\{.*?\}", "", text).strip()
