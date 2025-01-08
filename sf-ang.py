import ctypes

from src import static
from src.App import App
from src.ConfigManager import ConfigManager

# pyinstaller.exe --noconsole --onefile --add-data ".\src\template\month.docx;." .\sf-ang.py
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

    configManager = ConfigManager()
    logger = static.create_logger(configManager)

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(configManager.get_app_id()) #Setzt die App ID von dem Prozess

    app = App(logger,configManager) #Erstellt die App
    app.root.mainloop()#Loopt über die App