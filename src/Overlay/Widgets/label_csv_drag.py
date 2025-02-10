from PySide6 import QtWidgets
from pandas.io.common import file_path_to_url

from src.SettingManagement.ConfigManager import ConfigManager


class label_csv_drag(QtWidgets.QLabel):
    def __init__(self,parent = None, CM : ConfigManager = None):
        super().__init__(parent = parent)
        self.CM = CM
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0]
            if self.CM is not None:
                self.CM.set_csv_path(file_path_to_url(file_path.toLocalFile()))
            event.accept()
        else:
            event.ignore()

    def setCM(self, CM):
        self.CM = CM
