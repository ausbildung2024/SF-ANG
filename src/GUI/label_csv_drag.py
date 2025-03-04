from csv import excel

from PySide6 import QtWidgets
from pathlib import Path
from pandas.io.common import file_path_to_url

from src.Settings.ConfigManager import ConfigManager
from src.Utils.FileUtil import is_path_valid, is_file_valid


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
                #TODO Hier muss noch error correction rein!!!
                try:
                    file_path = file_path_to_url(file_path.toLocalFile())
                    is_file_valid(file_path,'.csv')
                    self.CM.set_csv_path(file_path)
                except Exception as e:
                    raise e
            event.accept()
        else:
            event.ignore()

    def setCM(self, CM):
        self.CM = CM
