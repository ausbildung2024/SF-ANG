import ctypes

import src.utils
from src.Overlay.App import App
from src.SettingManagement.ConfigManager import ConfigManager

if __name__ == "__main__":
    """
    Der Einstiegspunkt der Anwendung. Hier wird die PyQT-GUI gestartet und die Hauptanwendung geladen.
    """

    CM = ConfigManager()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(CM.get_app_id()) #Setzt die App ID von dem Prozess

    app = App(CM) #Erstellt die App