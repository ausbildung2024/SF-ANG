import ctypes
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from src.GUI.MainWindow import MainWindow
from src.Utils.CONSTANTS import APP_ID

"""
Der Einstiegspunkt der Anwendung. Hier wird die PyQT-GUI gestartet und die Hauptanwendung geladen.
"""
if __name__ == "__main__":

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID) #Setzt die App ID von dem Prozess

    qt_app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MainWindow()
    ui.setupUi(window)
    window.show()

    sys.exit(qt_app.exec())


