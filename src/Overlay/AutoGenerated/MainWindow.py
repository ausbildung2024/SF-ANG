# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sf_angwaXMwe.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QWidget)

from src.Overlay.Widgets.label_csv_drag import label_csv_drag

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(467, 303)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(467, 303))
        MainWindow.setMaximumSize(QSize(467, 303))
        MainWindow.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        MainWindow.setToolTipDuration(6)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gen_set_box = QGroupBox(self.centralwidget)
        self.gen_set_box.setObjectName(u"gen_set_box")
        self.gen_set_box.setGeometry(QRect(10, 10, 202, 88))
        self.gridLayout = QGridLayout(self.gen_set_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbl_lehrjahr = QLabel(self.gen_set_box)
        self.lbl_lehrjahr.setObjectName(u"lbl_lehrjahr")

        self.gridLayout.addWidget(self.lbl_lehrjahr, 0, 0, 1, 1)

        self.lbl_name = QLabel(self.gen_set_box)
        self.lbl_name.setObjectName(u"lbl_name")

        self.gridLayout.addWidget(self.lbl_name, 1, 0, 1, 1)

        self.name = QLineEdit(self.gen_set_box)
        self.name.setObjectName(u"name")

        self.gridLayout.addWidget(self.name, 1, 1, 1, 1)

        self.lehrjahr = QComboBox(self.gen_set_box)
        self.lehrjahr.addItem("")
        self.lehrjahr.addItem("")
        self.lehrjahr.addItem("")
        self.lehrjahr.setObjectName(u"lehrjahr")

        self.gridLayout.addWidget(self.lehrjahr, 0, 1, 1, 1)

        self.tmp_set_box = QGroupBox(self.centralwidget)
        self.tmp_set_box.setObjectName(u"tmp_set_box")
        self.tmp_set_box.setGeometry(QRect(230, 10, 231, 61))
        self.gridLayout_2 = QGridLayout(self.tmp_set_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tmp_date = QDateEdit(self.tmp_set_box)
        self.tmp_date.setObjectName(u"tmp_date")

        self.gridLayout_2.addWidget(self.tmp_date, 0, 1, 1, 1)

        self.lbl_tmp_date = QLabel(self.tmp_set_box)
        self.lbl_tmp_date.setObjectName(u"lbl_tmp_date")

        self.gridLayout_2.addWidget(self.lbl_tmp_date, 0, 0, 1, 1)

        self.quick_box = QGroupBox(self.centralwidget)
        self.quick_box.setObjectName(u"quick_box")
        self.quick_box.setGeometry(QRect(230, 80, 231, 101))
        self.formLayout = QFormLayout(self.quick_box)
        self.formLayout.setObjectName(u"formLayout")
        self.successfactor_but = QPushButton(self.quick_box)
        self.successfactor_but.setObjectName(u"successfactor_but")
        self.successfactor_but.setAutoRepeatDelay(300)
        self.successfactor_but.setAutoRepeatInterval(100)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.successfactor_but)

        self.appdata_but = QPushButton(self.quick_box)
        self.appdata_but.setObjectName(u"appdata_but")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.appdata_but)

        self.config_but = QPushButton(self.quick_box)
        self.config_but.setObjectName(u"config_but")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.config_but)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 99, 201, 81))
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gen_but_tmp = QPushButton(self.groupBox)
        self.gen_but_tmp.setObjectName(u"gen_but_tmp")

        self.gridLayout_4.addWidget(self.gen_but_tmp, 0, 1, 1, 1)

        self.gen_but = QPushButton(self.groupBox)
        self.gen_but.setObjectName(u"gen_but")
        self.gen_but.setAutoFillBackground(False)
        self.gen_but.setCheckable(False)

        self.gridLayout_4.addWidget(self.gen_but, 0, 0, 1, 1)

        self.csv_drop = label_csv_drag(self.centralwidget)
        self.csv_drop.setObjectName(u"csv_drop")
        self.csv_drop.setEnabled(True)
        self.csv_drop.setGeometry(QRect(10, 190, 451, 91))
        self.csv_drop.setMouseTracking(False)
        self.csv_drop.setAcceptDrops(True)
        self.csv_drop.setStyleSheet(u"border: 2px dashed #aaa")
        self.csv_drop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.lbl_lehrjahr.setBuddy(self.lehrjahr)
        self.lbl_name.setBuddy(self.name)
        self.lbl_tmp_date.setBuddy(self.tmp_date)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lehrjahr, self.name)
        QWidget.setTabOrder(self.name, self.gen_but)
        QWidget.setTabOrder(self.gen_but, self.tmp_date)
        QWidget.setTabOrder(self.tmp_date, self.gen_but_tmp)
        QWidget.setTabOrder(self.gen_but_tmp, self.successfactor_but)
        QWidget.setTabOrder(self.successfactor_but, self.appdata_but)

        self.retranslateUi(MainWindow)

        self.gen_but.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SF-ANG", None))
        self.gen_set_box.setTitle(QCoreApplication.translate("MainWindow", u"Allgemeine Einstellungen", None))
        self.lbl_lehrjahr.setText(QCoreApplication.translate("MainWindow", u"Lehrjahr", None))
        self.lbl_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.name.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Name des Auszubildenden </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lehrjahr.setItemText(0, QCoreApplication.translate("MainWindow", u"1 LJ", None))
        self.lehrjahr.setItemText(1, QCoreApplication.translate("MainWindow", u"2 LJ", None))
        self.lehrjahr.setItemText(2, QCoreApplication.translate("MainWindow", u"3 LJ", None))

#if QT_CONFIG(tooltip)
        self.lehrjahr.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auswahl des Lehrjahres</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tmp_set_box.setTitle(QCoreApplication.translate("MainWindow", u"Vorlage Dokument", None))
#if QT_CONFIG(tooltip)
        self.tmp_date.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auswahl des Monats und des Jahres f\u00fcr das die Vorlage erstellt werden soll</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tmp_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"MM.yyyy", None))
        self.lbl_tmp_date.setText(QCoreApplication.translate("MainWindow", u"Monat/Jahr", None))
        self.quick_box.setTitle(QCoreApplication.translate("MainWindow", u"QuickLinks", None))
#if QT_CONFIG(tooltip)
        self.successfactor_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet das Succes Factor im Browser (Nagarro Portal)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.successfactor_but.setText(QCoreApplication.translate("MainWindow", u"SuccessFactor", None))
#if QT_CONFIG(tooltip)
        self.appdata_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet den Appdata Ordner des Programms</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.appdata_but.setText(QCoreApplication.translate("MainWindow", u"AppData", None))
#if QT_CONFIG(tooltip)
        self.config_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet die Konfikurationsdatei des Programms</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.config_but.setText(QCoreApplication.translate("MainWindow", u"Config File", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Generieren", None))
#if QT_CONFIG(tooltip)
        self.gen_but_tmp.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Erstellt eine Ausbildungs Nachweis Vorlage basierent auf dem Vorlage Datum</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.gen_but_tmp.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.gen_but_tmp.setText(QCoreApplication.translate("MainWindow", u"Vorlage Erstellen", None))
#if QT_CONFIG(tooltip)
        self.gen_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Erstellt einen Ausbildungsnachweis basierend auf dem CSV File</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.gen_but.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.gen_but.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
#if QT_CONFIG(tooltip)
        self.csv_drop.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>CSV Datei aus von dem SuccessFactor hier hineinziehen</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.csv_drop.setText(QCoreApplication.translate("MainWindow", u"CSV Hier einf\u00fcgen", None))
    # retranslateUi

