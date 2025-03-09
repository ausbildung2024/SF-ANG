from src.Utils.CONSTANTS import *
"""
Lädt und manipuliert die Word-Dokument-Vorlage zur Erstellung von Nachweisen.
"""
class WordTemplate:

    """
    Initialisiert das WordTemplate-Objekt.

    Attribute:
        doc_path: Der pfad des Templates
    """
    def __init__(self, doc_path):
        self.document = Document(doc_path)

    """
    Ersetzt einen Platzhalter in einer Zelle des Dokuments durch einen Wert.
    """
    @staticmethod
    def replace_placeholders(cell, placeholder, value):
        if placeholder in cell.text:
            # Ersetzt den Platzhalter nur, wenn er in der Zelle vorhanden ist.
            cell.text = cell.text.replace(placeholder, str(value))

    """
    Ersetzt mehrere Platzhalter in einer Zelle basierend auf einem Dictionary von Platzhaltern und Werten.
    
    Parameter:
        cell: Die Zelle des Word Dokuments
        placeholder: Die Platzhalter die ausgetauscht werden sollen
    """
    def replace_general_placeholders(self, cell, placeholders):
        for placeholder, value in placeholders.items():
            # Iteriert durch alle Platzhalter und ersetzt sie in der Zelle.
            self.replace_placeholders(cell, placeholder, value)

    """
    Speichert das Word-Dokument in einem angegebenen Ordner und fügt einen Zeitstempel zum Dateinamen hinzu
    
    Parameter:
        output_folder: Den Pfad zum speichern des Dokuments
    """
    def save_document(self, output_folder):
        output_folder.mkdir(parents=True, exist_ok=True)  # Erstellt den Ordner, falls er nicht existiert
        timestamp = datetime.now().strftime(WORD_TIME)  # Generiert einen Zeitstempel
        output_path = output_folder / WORD_NAME.format(timestamp)  # Setzt den Dateinamen

        try:
            self.document.save(output_path)
        except Exception as e:
            # Fehler beim Speichern
            pass
        return output_path
