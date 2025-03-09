from src.Utils.CONSTANTS import *

class LabelCsvDrag(QtWidgets.QLabel):
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.mainWindow = None
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
            if self.mainWindow is not None:
                try:
                    file_path = event_path_to_path(event)
                    is_file_valid(file_path,FILETYPE_CSV)
                    self.mainWindow.set_csv_path(file_path.as_posix())
                except Exception as e:
                    create_error_dialog(str(e))
                else:
                    create_success_dialog(SCC_CSV_LO)

            event.accept()
        else:
            event.ignore()

    def set_main_window(self, main_window):
        self.mainWindow = main_window
