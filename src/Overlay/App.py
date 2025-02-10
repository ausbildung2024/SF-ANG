import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from src.Overlay.MainWindow import MainWindow
from src.SettingManagement.ConfigManager import ConfigManager


class App:
    def __init__(self,configManager: ConfigManager):
        self.CM = configManager
        self.logger = self.CM.get_logger()

        self.qt_app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.ui = MainWindow(self.CM)
        self.ui.setupUi(self.win)
        self.win.show()

        sys.exit(self.qt_app.exec_())