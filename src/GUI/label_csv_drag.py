from csv import excel

from PySide6 import QtWidgets
from pathlib import Path

from src.Settings.ConfigManager import ConfigManager
from src.Utils.FileUtil import is_path_valid, is_file_valid, event_path_to_path
from src.Utils.UiUtils import create_error_dialog, create_success_dialog


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
            if self.CM is not None:
                try:
                    file_path = event_path_to_path(event)
                    is_file_valid(file_path,'.csv')
                    self.CM.set_csv_path(file_path.as_posix())
                except Exception as e:
                    create_error_dialog(str(e))
                else:
                    create_success_dialog("File erfolgreich geladen!")

            event.accept()
        else:
            event.ignore()

    def setCM(self, CM):
        self.CM = CM