import ctypes
import tkinter as tk  # Importiert das Tkinter-Modul für die GUI-Erstellung

from src.App import App  # Importiert die App-Klasse aus dem src.App-Modul, die die Hauptanwendungslogik enthält
from src.ConfigManagerOld import *

# pyinstaller.exe --noconsole --onefile --add-data ".\src\template\month.docx;." .\main.py
# Diese Zeile ist ein Kommentar und stellt den Befehl dar, der verwendet wird, um das Python-Skript mit PyInstaller
# in eine eigenständige EXE-Datei zu kompilieren. Der Befehl gibt an:
# - --noconsole: Verhindert das Öffnen eines Konsolenfensters, wenn die EXE ausgeführt wird
# - --onefile: Erzeugt eine einzelne ausführbare Datei, die alle Abhängigkeiten enthält
# - --add-data: Fügt zusätzliche Dateien (in diesem Fall die Word-Vorlage "month.docx") zur EXE hinzu
# Der Befehl stellt sicher, dass die Vorlage in der erstellten EXE enthalten ist, auch wenn die Datei im Code referenziert wird.

if __name__ == "__main__":
    """
    Der Einstiegspunkt der Anwendung. Hier wird die Tkinter-GUI gestartet und die Hauptanwendung geladen.
    """

    myappid = 'ausbildung24.generator.' + APP_NAME + APP_VERSION  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Erstellt ein Tkinter-Hauptfenster, das als Container für die GUI-Elemente dient
    root = tk.Tk()

    # Initialisiert die App-Klasse und übergibt das Tkinter-Hauptfenster als Argument
    # Die App-Klasse übernimmt dann die Erstellung und Verwaltung der gesamten Benutzeroberfläche
    app = App(root)

    # Startet die Tkinter-Ereignisschleife, die auf Benutzerinteraktionen wartet und die GUI anzeigt.
    # Diese Schleife bleibt aktiv, solange das Fenster offen ist.
    root.mainloop()
