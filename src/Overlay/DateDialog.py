from tkinter import simpledialog
from tkinter import ttk
import tkinter as tk

class DateDialog(simpledialog.Dialog):
    def body(self, master):
        # Layout des Dialogs definieren
        tk.Label(master, text="Jahr:").grid(row=0)
        tk.Label(master, text="Monat:").grid(row=1)

        self.year_combobox = ttk.Combobox(master, values=[str(year) for year in range(2025, 2031)])
        self.month_combobox = ttk.Combobox(master, values=[str(month) for month in range(1, 13)])

        self.year_combobox.grid(row=0, column=1)
        self.month_combobox.grid(row=1, column=1)

        self.year_combobox.current(0)  # Standardwert setzen
        self.month_combobox.current(0)  # Standardwert setzen

        return self.year_combobox  # Fokus auf das Jahr-Combobox setzen

    def apply(self):
        # Aktion ausführen, wenn der Benutzer den Dialog bestätigt
        self.year = self.year_combobox.get()
        self.month = self.month_combobox.get()
