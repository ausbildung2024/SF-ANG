import os
import sys
import pywinstyles
import tkinter as tk
import sv_ttk
import darkdetect
import webbrowser
from logging import Logger
from pathlib import Path

from dateutil.rrule import weekday

from src import static
from src.SettingsHandler import ConfigManager
from tkinter import messagebox, filedialog
from src.WeekDataProcessor import WeekDataProcessor
from src.WordTemplate import WordTemplate


class App:
    def __init__(self, logger: Logger, configManager: ConfigManager):
        self.CM = configManager

        self.root = tk.Tk() # Setzen des Hauptfensters der UI
        self.root.title(self.CM.get_app_name()) #Setzt den Titel der App
        self.menubar = tk.Menu(self.root)
        self.root.geometry("236x195")
        self.root.resizable(False, False)


        self.logger = logger

        self.set_icon() # Setzt das Icon

        # erstellen der Variablen welche dargestellt werden
        self.name_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.hour_var = tk.StringVar()
        self.csv_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.template_path = tk.StringVar()

        self.generate_interface() # Generiert das UI

    """
    Generiert die eizelnen Elemente des UI's
    """
    def generate_interface(self):

        # Generiert eingabefelder für die Einstellungen
        self.label_entry_helper(0, self.CM.get_label('name'), self.name_var)
        self.label_entry_helper(1, self.CM.get_label('year'), self.year_var)
        self.label_entry_helper(2, self.CM.get_label('hour'), self.hour_var)

        # Generiert Felder für das setzen der Pfade
        self.file_selector_helper(3,self.CM.get_label('csv'), self.csv_path,self.get_csv_path )
        self.file_selector_helper(4,self.CM.get_label('template'), self.template_path,self.get_template_path)
        self.file_selector_helper(5,self.CM.get_label('output'), self.output_path,self.get_output_path)

        # Generiert den Knopf der das Generieren bestätigt:
        tk.Button(self.root, text=self.CM.get_label('generate'), command=self.generate_document).grid(row=6, column=1)

        #tk.Button(self.root, text="Leere Vorlage", command=self.empty_document).grid(row=6, column=0)

        # Setzen der Standard Werte
        self.name_var.set(self.CM.get_name())
        self.year_var.set(self.CM.get_year())
        self.hour_var.set(self.CM.get_default_hours())

        self.csv_path.set(self.CM.get_csv_path())
        self.template_path.set(self.CM.get_template_path())
        self.output_path.set(self.CM.get_output_path())

        #Erstellt die Menu bar
        self.generate_menu_bar()

        #Setzt das Theme
        self.set_theme()

    """
    Setzt das Theme so wie es in den einstellungen konfiguriert wurde
    """
    def set_theme(self,theme = 'nt'):
        #Setzen des Themes wenn es übergeben wird
        if theme != 'nt':
            self.CM.set_theme(theme)

        #Aufrufen des Themes
        theme = self.CM.get_theme()
        if theme == 'dark' or theme == 'light':
            sv_ttk.set_theme(theme)
        else:
            sv_ttk.set_theme(darkdetect.theme())
        self.apply_theme_to_titlebar()


    """
    Setzt Das Theme auch für die Titlebar
    """
    def apply_theme_to_titlebar(self):
        version = sys.getwindowsversion()
        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(self.root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(self.root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            self.root.wm_attributes("-alpha", 0.99)
            self.root.wm_attributes("-alpha", 1)

    """
    Erstellt eine Menubar für das Fenster
    """
    def generate_menu_bar(self):
        self.root.config(menu=self.menubar)

        self.add_settings_menu()
        self.add_theme_menu()
        self.add_help_menu()

    def add_help_menu(self):
        help_menu = tk.Menu(self.root, tearoff=False)

        self.menubar.add_cascade(
            label="About",
            menu=help_menu
        )

        help_menu.add_command(
            label="Auf Updates überprüfen",
            #command=
        )

        help_menu.add_command(
            label="Help",
            #command=
        )


    def add_settings_menu(self):

        settings_menu = tk.Menu(self.root,tearoff=False)



        self.menubar.add_cascade(
            label="Settings",
            menu=settings_menu
        )

        settings_menu.add_separator()

        settings_menu.add_command(
            label="Portal",
            command=self.open_portal
        )

        settings_menu.add_command(
            label="Appdata",
            command=self.open_programm_files

        )

        settings_menu.add_command(
            label="Config File",
            command=self.open_config_file

        )

        settings_menu.add_separator()

        settings_menu.add_command(
            label='Exit',
            command=self.root.destroy,
        )

    def add_theme_menu(self):

        theme_menu = tk.Menu(self.root,tearoff=False)

        self.menubar.add_cascade(
            label="Theme",
            menu=theme_menu
        )

        theme_menu.add_command(
            label='Dark',
            command=lambda: self.set_theme('dark')
        )

        theme_menu.add_command(
            label='Light',
            command=lambda: self.set_theme('light')
        )

        theme_menu.add_command(
            label='System',
            command=lambda: self.set_theme('auto')
        )

    """
    Öffnet den 
    """
    def open_config_file(self):
        os.startfile(self.CM.get_config_path())

    """
    Öffnet Den Programm Ordner in APP_DATA
    """
    def open_programm_files(self):
        os.startfile(self.CM.get_appdata_path())

    """
    Setzt das Icon für die Taskbar
    """
    def set_icon(self):
        icon_small = tk.PhotoImage(file = self.CM.get_app_icon('small'))
        icon_big = tk.PhotoImage(file = self.CM.get_app_icon('large'))
        self.root.iconphoto(False, icon_big, icon_small)

    """
    Helfermethode zum generieren eines labels zusammen mit einem Eingabefeld
    """
    def label_entry_helper(self, row, label_text,textvariable, column = 0):
        label = tk.Label(self.root, text = label_text)
        entry = tk.Entry(self.root, textvariable = textvariable)

        label.grid(row = row, column = column)
        entry.grid(row = row, column = column + 1)


    """
    Öffnet ein Pop Up zum auswählen einer datei/ordner
    """
    def file_chooser(self, path, filetypes = None):
        path_str = path.get()

        # Falls schon ein file z.B xxx/file.txt gewählt wurde soll dieser entfern werden, so das nurnoch die Ordnerstruktur im Pfad steht
        if path_str.find('.') !=-1:
            path_str = Path(path.get()).parent.absolute()

        # Wählen der richtigen methode, wenn filetypes none ist können nur ordner gewählt werden
        if filetypes is None:
            new_path = filedialog.askopenfilename(initialdir = path_str)
        else:
            new_path = filedialog.askopenfilename(filetypes=filetypes, initialdir=path_str)

        # Falls ein Pfad ausgewählt wird, wird dieser gesetzt
        if new_path != "":
            path.set(new_path)

    """
    Methode zum öffnen des CSV Pfad
    """
    def get_csv_path(self):
        self.file_chooser(self.csv_path,self.CM.get_filetype('csv'))

    """
    Methode zum öffnen des output Pfad
    """
    def get_output_path(self):
        new_dir = filedialog.askdirectory(initialdir=self.output_path.get())
        self.output_path.set(new_dir)

    """
    Methode zum öffnen des template Pfad
    """
    def get_template_path(self):
        self.file_chooser(self.template_path,self.CM.get_filetype('word'))

    """
    Helfermethode zum generieren eines labels zusammen mit einem ausgabe Feld und einen Knopf
    """
    def file_selector_helper(self, row, label_text, textvariable, command, column = 0):
        label = tk.Label(self.root, text=label_text)

        button = tk.Button(self.root, text=self.CM.get_label('select'), command=command)

        label.grid(row=row, column=column)
        button.grid(row=row, column=column + 1)

    def empty_document(self):

        self.generate_document(True)

    """
    Lädt die CSV und die Vorlage um daraus ein Fertiges Dokument zu generieren
    """
    def generate_document(self, empty = False):
        self.update_config()

        template = self.load_template()
        if not empty:
            csv = self.load_csv()
        else:
            csv = None

        week_processor = WeekDataProcessor(self.logger, self.CM, template, csv)
        week_processor.process_all_weeks()  # Verarbeitet alle Wochendaten aus der CSV und füllt die Vorlage

        try:
            output_path = template.save_document(Path(self.output_path.get()))
            self.show_success("Dokument erfolgreich erstellt.")
            os.startfile(output_path)
        except Exception as e:
            self.show_error(f"Fehler beim Speichern des Dokuments: {e}")


    """
    Öffnet Direkt das Nagarro Portal
    """
    def open_portal(self):
        webbrowser.open(self.CM.get_portal_link(), new= 0, autoraise=True)

    """
    Lädt die daten aus der csv datei (von Successfactor generiert)
    """
    def load_csv(self):
        csv_data = static.load_csv(self.CM,self.logger, Path(self.csv_path.get()))
        if csv_data is None:  # Falls das Laden der CSV-Daten fehlschlägt, wird eine Fehlermeldung angezeigt
            self.show_error("Fehler beim Laden der CSV-Datei.")
            return
        return csv_data

    """
    Lädt die Template word Datei
    """
    def load_template(self):
        word_template = WordTemplate(self.logger, Path(self.template_path.get()))
        if word_template.document is None:  # Falls das Laden der Word-Vorlage fehlschlägt, wird eine Fehlermeldung angezeigt
            self.show_error("Fehler beim Laden der Vorlage.")
            return
        return word_template

    """
    Zeigt ein Fehler Pop-Up Fenster an
    """
    def show_error(self, message):
        messagebox.showerror(self.CM.get_label('fehler'), message)
        self.logger.error(message)

    """
    Zeigt ein erfolgs Pop-Up fenster an
    """
    def show_success(self, message):
        messagebox.showinfo(self.CM.get_label('erfolg'), message)
        self.logger.info(message)

    """
    Updated den config file mit den eingegebenen werten (name, jahr, standard stunden)
    """
    def update_config(self):
        self.CM.set_name(self.get_name())
        self.CM.set_year(self.get_year())
        self.CM.set_default_hours(self.get_default_hours())

    """
    Getter für den namen
    """
    def get_name(self):
        return self.name_var.get()

    """
    Getter für das Ausbildungsjahr
    """
    def get_year(self):
        return self.year_var.get()

    """
    Getter für die Default Hours
    """
    def get_default_hours(self):
        return self.hour_var.get()