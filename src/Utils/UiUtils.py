from PySide6 import QtWidgets

"""
Erstellt einen Dialog mit Titel und Nachricht

Attribute:
    msg: Die anzuzeigende nachricht
    title: Der Titel des Dialog Fensters
"""
def create_dialog(msg,title):
    error_dialog = QtWidgets.QErrorMessage()
    # Freezed das Hauptfenster wenn die Message angezeigt wird
    error_dialog.setModal(True)
    # Setzt die Strings des Fensters
    error_dialog.setWindowTitle(title)
    error_dialog.showMessage(msg)
    # Führt den Dialog aus
    error_dialog.exec_()

"""
Erstellt einen Fehler Dialog

Attribute:
    err_msg: Die anzuzeigende Fehlernachricht
"""
def create_error_dialog(err_msg):
    create_dialog(err_msg,"Ein Fehler ist aufgetreten!")
<r
"""
Erstellt einen Erfolg Dialog

Attribute:
    scc_msg: Die anzuzeigende Erfolgsnachricht
"""
def create_success_dialog(scc_msg):
    create_dialog(scc_msg,"Erfolg!")
