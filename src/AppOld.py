import sys
import tkinter as tk
from tkinter import messagebox, filedialog

from src.CSVLoader import CSVLoader  # Dienst zum Laden und Validieren von CSV-Daten aus einer CSV-Datei
from src.ConfigManagerOld import *  # Konfigurationsmanager zum Laden und Speichern von Anwendungseinstellungen
from src.Logger import Logger  # Logger zur Protokollierung von Informationen und Fehlern
from src.WeekDataProcessor import \
    WeekDataProcessor  # Dienst zur Verarbeitung der CSV-Daten und Aufbereitung für das Dokument
from src.WordTemplate import WordTemplate  # Dienst zum Laden und Bearbeiten der Word-Dokumentvorlage


# Hauptklasse der Anwendung
class App:
    def __init__(self, root):
        """
        Initialisiert die Hauptanwendung, lädt die Einstellungen und erstellt alle GUI-Komponenten.

        Parameter:
        - root: Das Hauptfenster (Tkinter root), das als Basis für die GUI-Komponenten dient.
        """
        # Lädt die Anwendungseinstellungen aus der Konfigurationsdatei
        self.settings = settings
        self.root = root  # Setzt das Hauptfenster für die GUI
        self.root.title(APP_NAME)  # Setzt den Fenstertitel für die Anwendung

        # Initialisiert den Logger und legt den Speicherort des Log-Verzeichnisses fest
        log_folder = self.settings.get('log_folder', './logs')
        self.logger = Logger(log_folder).get_logger()

        # Definiert die Standardpfade für CSV-Datei, Word-Vorlage und das Ausgabeverzeichnis
        self.csv_path = Path.cwd() / self.settings.get('input_csv')

        icon_small = tk.PhotoImage(file= Path.cwd() / 'res/pictures/icon_16x.png')
        icon_big = tk.PhotoImage(file= Path.cwd() / 'res/pictures/icon_32x.png')
        self.root.iconphoto(False, icon_big, icon_small)

        # Prüft, ob die Anwendung über PyInstaller als `.exe` läuft, indem das `_MEIPASS` Attribut in `sys` gesucht wird.
        # Wenn `_MEIPASS` vorhanden ist, wird der Pfad zu `month.docx` gesetzt (Pfad für exe). Andernfalls Standardpfad.
        if hasattr(sys, '_MEIPASS'):
            self.template_path = Path(sys._MEIPASS) / 'month.docx'
        else:
            self.template_path = Path.cwd() / self.settings.get('template')
        # Setzt das Standard-Ausgabeverzeichnis auf das aktuelle Arbeitsverzeichnis
        self.output_folder = Path.cwd()

        # Erstellen der GUI-Komponenten, die der Benutzer im Fenster sehen kann
        self.create_widgets()

    def create_widgets(self):
        """
        Baut die Benutzeroberfläche der Anwendung auf, einschließlich aller Labels, Buttons und Eingabefelder
        für Datei- und Ordnerauswahl, sowie des Buttons zur Erstellung des Berichts.
        """
        # Label und Button zur Auswahl der CSV-Datei
        tk.Label(self.root, text="CSV-Datei auswählen:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Button(self.root, text="Durchsuchen", command=self.select_csv).grid(row=0, column=1, padx=5, pady=5)
        # Label zur Anzeige des aktuellen Pfads der ausgewählten CSV-Datei
        self.csv_path_label = tk.Label(self.root, text=f"CSV Pfad: {self.csv_path}")
        self.csv_path_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Label und Button zur Auswahl der Word-Vorlage
        tk.Label(self.root, text="Word-Vorlage auswählen:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Button(self.root, text="Durchsuchen", command=self.select_template).grid(row=1, column=1, padx=5, pady=5)
        # Label zur Anzeige des aktuellen Pfads der ausgewählten Word-Vorlage
        self.template_path_label = tk.Label(self.root, text=f"Vorlage Pfad: {self.template_path}")
        self.template_path_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Label und Button zur Auswahl des Ausgabeordners
        tk.Label(self.root, text="Ausgabeordner auswählen:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Button(self.root, text="Durchsuchen", command=self.select_output_folder).grid(row=2, column=1, padx=5,
                                                                                         pady=5)
        # Label zur Anzeige des aktuellen Pfads des ausgewählten Ausgabeordners
        self.output_folder_label = tk.Label(self.root, text=f"Ausgabeordner: {self.output_folder}")
        self.output_folder_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Button zur Erstellung des Berichts, der die generate_report-Methode aufruft
        tk.Button(self.root, text="Erstellen", command=self.generate_report).grid(row=3, column=0, columnspan=2, padx=5,
                                                                                  pady=5)

    def select_csv(self):
        """
        Öffnet einen Dateiauswahldialog für die CSV-Datei und aktualisiert den Pfad.
        Zeigt den ausgewählten CSV-Pfad im entsprechenden Label an.
        """
        # Öffnet den Dialog zum Auswählen der CSV-Datei
        path = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")], initialdir=Path.cwd())
        if path:  # Wenn ein Pfad ausgewählt wurde, wird er aktualisiert
            self.csv_path = Path(path)
            self.logger.info(f"CSV-Datei ausgewählt: {self.csv_path}")  # Protokolliert die Auswahl der CSV-Datei
            self.csv_path_label.config(
                text=f"CSV Pfad: {self.csv_path}")  # Aktualisiert das Label zur Anzeige des neuen Pfads

    def select_template(self):
        """
        Öffnet einen Dateiauswahldialog für die Word-Vorlage und aktualisiert den Pfad.
        Zeigt den ausgewählten Vorlagenpfad im entsprechenden Label an.
        """
        # Öffnet den Dialog zum Auswählen der Word-Vorlage
        path = filedialog.askopenfilename(filetypes=[("Word-Dokumente", "*.docx")], initialdir=Path.cwd())
        if path:  # Wenn ein Pfad ausgewählt wurde, wird er aktualisiert
            self.template_path = Path(path)
            self.logger.info(f"Vorlage ausgewählt: {self.template_path}")  # Protokolliert die Auswahl der Word-Vorlage
            self.template_path_label.config(
                text=f"Vorlage Pfad: {self.template_path}")  # Aktualisiert das Label zur Anzeige des neuen Pfads

    def select_output_folder(self):
        """
        Öffnet einen Ordnerauswahldialog für das Ausgabeverzeichnis und aktualisiert den Pfad.
        Zeigt den ausgewählten Ordnerpfad im entsprechenden Label an.
        """
        # Öffnet den Dialog zum Auswählen des Ausgabeordners
        path = filedialog.askdirectory(initialdir=Path.cwd())
        if path:  # Wenn ein Pfad ausgewählt wurde, wird er aktualisiert
            self.output_folder = Path(path)
            self.logger.info(
                f"Ausgabeordner ausgewählt: {self.output_folder}")  # Protokolliert die Auswahl des Ausgabeordners
            self.output_folder_label.config(
                text=f"Ausgabeordner: {self.output_folder}")  # Aktualisiert das Label zur Anzeige des neuen Pfads

    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung in einem Popup-Fenster an.

        Parameter:
        - message: Die anzuzeigende Fehlermeldung als Text.
        """
        # Zeigt das übergebene Fehlernachricht als Popup an
        messagebox.showerror("Fehler", message)

    def generate_report(self):
        """
        Startet die Berichtserstellung, indem sie die Pfadauswahl überprüft, die CSV-Daten lädt,
        die Word-Vorlage bearbeitet, die Daten verarbeitet und das ausgefüllte Dokument speichert.
        Zeigt nach erfolgreicher Erstellung oder bei Fehlern entsprechende Meldungen an.

        Ablauf:
        1. Überprüft, ob die erforderlichen Dateien und Ordner ausgewählt wurden.
        2. Lädt die CSV-Daten aus der ausgewählten Datei.
        3. Lädt die Word-Vorlage, in die die Daten eingefügt werden sollen.
        4. Verarbeitet die CSV-Daten und füllt die Word-Vorlage mit den relevanten Informationen.
        5. Speichert das Dokument und erstellt ein Backup.
        6. Zeigt dem Benutzer eine Erfolgsmeldung oder eine Fehlermeldung an, je nachdem, ob der Prozess erfolgreich war.
        """
        # Überprüfen, ob alle erforderlichen Pfade (CSV, Vorlage und Ausgabeordner) korrekt gesetzt sind.
        if not all([self.csv_path, self.template_path, self.output_folder]):
            # Falls nicht alle Pfade gesetzt sind, wird eine Fehlermeldung angezeigt und der Vorgang abgebrochen.
            self.show_error("Bitte wählen Sie alle erforderlichen Dateien und Ordner aus.")
            return

        # Aktualisieren der App-Einstellungen mit den für diesen Lauf ausgewählten Pfaden
        # Diese Einstellungen werden genutzt, um den Pfad zu CSV, Vorlage und Ausgabeordner zu speichern.
        self.settings['input_csv'] = self.csv_path
        self.settings['template'] = self.template_path
        self.settings['output_folder'] = self.output_folder
        # Falls im Settings keine `output_backup` definiert ist, wird der Standardwert (Backup im Ausgabeordner) gesetzt.
        self.settings['output_backup'] = self.settings.get('output_backup', self.output_folder / "backup")

        # Initialisierung des CSVLoaders, um die CSV-Daten zu laden
        csv_loader = CSVLoader(self.logger, self.settings['input_csv'])
        csv_data = csv_loader.load()  # Laden der CSV-Daten aus der Datei
        if csv_data is None:  # Falls das Laden der CSV-Daten fehlschlägt, wird eine Fehlermeldung angezeigt
            self.show_error("Fehler beim Laden der CSV-Datei.")
            return

        # Initialisierung des WordTemplate-Objekts, um die Word-Vorlage zu laden und zu bearbeiten
        word_template = WordTemplate(self.logger, self.settings['template'])
        if word_template.document is None:  # Falls das Laden der Word-Vorlage fehlschlägt, wird eine Fehlermeldung angezeigt
            self.show_error("Fehler beim Laden der Vorlage.")
            return

        # Verarbeiten der geladenen CSV-Daten mit der WeekDataProcessor-Klasse
        # Diese Klasse übernimmt das Befüllen der Word-Vorlage mit den Daten aus der CSV
        week_processor = WeekDataProcessor(self.logger, self.settings, word_template, csv_data)
        week_processor.process_all_weeks()  # Verarbeitet alle Wochendaten aus der CSV und füllt die Vorlage

        # Versuch, das ausgefüllte Dokument zu speichern
        try:
            # Speichern des bearbeiteten Dokuments im festgelegten Ausgabeverzeichnis
            output_path = word_template.save_document(self.settings['output_folder'])
            # Zusätzliches Backup des Dokuments im festgelegten Backup-Verzeichnis
            word_template.save_document(self.settings['output_backup'])
            # Zeigt eine Erfolgsmeldung an, wenn das Dokument erfolgreich erstellt wurde
            messagebox.showinfo("Erfolg", "Dokument erfolgreich erstellt.")
            # Öffnet das Dokument im Dateimanager (z. B. Explorer) für den Benutzer
            os.startfile(output_path)
        except Exception as e:
            # Falls ein Fehler beim Speichern des Dokuments auftritt, wird dieser im Log protokolliert
            self.logger.error(f"Fehler beim Speichern des Dokuments: {e}")
            # Zeigt eine Fehlermeldung an, wenn beim Speichern des Dokuments ein Problem auftritt
            self.show_error("Fehler beim Speichern des Dokuments.")
