import ctypes
import sys

from src.Settings.logger import *
from PySide6.QtWidgets import QApplication, QMainWindow
from src.GUI.MainWindow import MainWindow
from src.Settings.ConfigManager import ConfigManager

if __name__ == "__main__":
    """
    Der Einstiegspunkt der Anwendung. Hier wird die PyQT-GUI gestartet und die Hauptanwendung geladen.
    """

    CM = ConfigManager()

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(CM.get_app_id()) #Setzt die App ID von dem Prozess

    qt_app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow(CM)
    ui.setupUi(window)
    window.show()

    sys.exit(qt_app.exec())


