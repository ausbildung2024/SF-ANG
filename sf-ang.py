import ctypes
from src.Utils import static
from src.Overlay.App import App
from src.SettingManagement.SettingsHandler import ConfigManager

if __name__ == "__main__":
    """
    Der Einstiegspunkt der Anwendung. Hier wird die Tkinter-GUI gestartet und die Hauptanwendung geladen.
    """

    configManager = ConfigManager()
    logger = static.create_logger(configManager)

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(configManager.get_app_id()) #Setzt die App ID von dem Prozess

    app = App(logger,configManager) #Erstellt die App
    app.root.mainloop()#Loopt über die App