import ctypes
from src.App import App
from src.ConfigData import settings

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
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(settings['app']['id'])

    app = App()

    app.root.mainloop()