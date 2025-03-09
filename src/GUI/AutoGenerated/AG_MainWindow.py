# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sf_angsQEGCJ.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

from src.GUI.LabelCsvDrag import LabelCsvDrag

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(586, 260)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(522, 260))
        MainWindow.setMaximumSize(QSize(4000, 4000))
        MainWindow.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        MainWindow.setToolTipDuration(6)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.quick_box = QGroupBox(self.centralwidget)
        self.quick_box.setObjectName(u"quick_box")
        self.gridLayout_3 = QGridLayout(self.quick_box)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.successfactor_but = QPushButton(self.quick_box)
        self.successfactor_but.setObjectName(u"successfactor_but")
        self.successfactor_but.setAutoRepeatDelay(300)
        self.successfactor_but.setAutoRepeatInterval(100)

        self.gridLayout_3.addWidget(self.successfactor_but, 0, 0, 1, 1)

        self.config_but = QPushButton(self.quick_box)
        self.config_but.setObjectName(u"config_but")

        self.gridLayout_3.addWidget(self.config_but, 0, 1, 1, 1)

        self.appdata_but = QPushButton(self.quick_box)
        self.appdata_but.setObjectName(u"appdata_but")

        self.gridLayout_3.addWidget(self.appdata_but, 1, 0, 1, 1)

        self.save_but = QPushButton(self.quick_box)
        self.save_but.setObjectName(u"save_but")

        self.gridLayout_3.addWidget(self.save_but, 1, 1, 1, 1)


        self.gridLayout_5.addWidget(self.quick_box, 1, 0, 1, 1)

        self.gen_set_box = QGroupBox(self.centralwidget)
        self.gen_set_box.setObjectName(u"gen_set_box")
        self.gridLayout = QGridLayout(self.gen_set_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbl_lehrjahr = QLabel(self.gen_set_box)
        self.lbl_lehrjahr.setObjectName(u"lbl_lehrjahr")

        self.gridLayout.addWidget(self.lbl_lehrjahr, 0, 0, 1, 1)

        self.lehrjahr = QComboBox(self.gen_set_box)
        self.lehrjahr.addItem("")
        self.lehrjahr.addItem("")
        self.lehrjahr.addItem("")
        self.lehrjahr.setObjectName(u"lehrjahr")

        self.gridLayout.addWidget(self.lehrjahr, 0, 1, 1, 1)

        self.lbl_name = QLabel(self.gen_set_box)
        self.lbl_name.setObjectName(u"lbl_name")

        self.gridLayout.addWidget(self.lbl_name, 1, 0, 1, 1)

        self.name = QLineEdit(self.gen_set_box)
        self.name.setObjectName(u"name")

        self.gridLayout.addWidget(self.name, 1, 1, 1, 1)


        self.gridLayout_5.addWidget(self.gen_set_box, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.csv_drop = LabelCsvDrag(self.groupBox_2)
        self.csv_drop.setObjectName(u"csv_drop")
        self.csv_drop.setEnabled(True)
        self.csv_drop.setMouseTracking(False)
        self.csv_drop.setAcceptDrops(True)
        self.csv_drop.setStyleSheet(u"border: 2px dashed #aaa")
        self.csv_drop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.csv_drop, 0, 0, 1, 1)

        self.gen_but = QPushButton(self.groupBox_2)
        self.gen_but.setObjectName(u"gen_but")
        self.gen_but.setAutoFillBackground(False)
        self.gen_but.setCheckable(False)

        self.gridLayout_4.addWidget(self.gen_but, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_2, 0, 1, 2, 1)

        self.tmp_set_box = QGroupBox(self.centralwidget)
        self.tmp_set_box.setObjectName(u"tmp_set_box")
        self.gridLayout_2 = QGridLayout(self.tmp_set_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cb_vorlage_montag = QCheckBox(self.tmp_set_box)
        self.cb_vorlage_montag.setObjectName(u"cb_vorlage_montag")

        self.verticalLayout.addWidget(self.cb_vorlage_montag)

        self.cb_vorlage_dienstag = QCheckBox(self.tmp_set_box)
        self.cb_vorlage_dienstag.setObjectName(u"cb_vorlage_dienstag")

        self.verticalLayout.addWidget(self.cb_vorlage_dienstag)

        self.cb_vorlage_mittwoch = QCheckBox(self.tmp_set_box)
        self.cb_vorlage_mittwoch.setObjectName(u"cb_vorlage_mittwoch")

        self.verticalLayout.addWidget(self.cb_vorlage_mittwoch)

        self.cb_vorlage_freitag = QCheckBox(self.tmp_set_box)
        self.cb_vorlage_freitag.setObjectName(u"cb_vorlage_freitag")

        self.verticalLayout.addWidget(self.cb_vorlage_freitag)

        self.cb_vorlage_Freitag = QCheckBox(self.tmp_set_box)
        self.cb_vorlage_Freitag.setObjectName(u"cb_vorlage_Freitag")

        self.verticalLayout.addWidget(self.cb_vorlage_Freitag)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.lbl_tmp_date = QLabel(self.tmp_set_box)
        self.lbl_tmp_date.setObjectName(u"lbl_tmp_date")

        self.gridLayout_2.addWidget(self.lbl_tmp_date, 0, 0, 1, 1)

        self.tmp_date = QDateEdit(self.tmp_set_box)
        self.tmp_date.setObjectName(u"tmp_date")

        self.gridLayout_2.addWidget(self.tmp_date, 0, 1, 1, 1)

        self.label = QLabel(self.tmp_set_box)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.gen_but_tmp = QPushButton(self.tmp_set_box)
        self.gen_but_tmp.setObjectName(u"gen_but_tmp")

        self.gridLayout_2.addWidget(self.gen_but_tmp, 2, 0, 1, 2)


        self.gridLayout_5.addWidget(self.tmp_set_box, 0, 2, 2, 1)

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
        QWidget.setTabOrder(self.name, self.tmp_date)
        QWidget.setTabOrder(self.tmp_date, self.successfactor_but)
        QWidget.setTabOrder(self.successfactor_but, self.appdata_but)

        self.retranslateUi(MainWindow)

        self.gen_but.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SF-ANG", None))
        self.quick_box.setTitle(QCoreApplication.translate("MainWindow", u"QuickLinks", None))
#if QT_CONFIG(tooltip)
        self.successfactor_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet das Succes Factor im Browser (Nagarro Portal)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.successfactor_but.setText(QCoreApplication.translate("MainWindow", u"SuccessFactor", None))
#if QT_CONFIG(tooltip)
        self.config_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet die Konfikurationsdatei des Programms</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.config_but.setText(QCoreApplication.translate("MainWindow", u"Config File", None))
#if QT_CONFIG(tooltip)
        self.appdata_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u00d6ffnet den Appdata Ordner des Programms</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.appdata_but.setText(QCoreApplication.translate("MainWindow", u"AppData", None))
        self.save_but.setText(QCoreApplication.translate("MainWindow", u"Einst. Speichern", None))
        self.gen_set_box.setTitle(QCoreApplication.translate("MainWindow", u"Allgemeine Einstellungen", None))
        self.lbl_lehrjahr.setText(QCoreApplication.translate("MainWindow", u"Lehrjahr", None))
        self.lehrjahr.setItemText(0, QCoreApplication.translate("MainWindow", u"1 LJ", None))
        self.lehrjahr.setItemText(1, QCoreApplication.translate("MainWindow", u"2 LJ", None))
        self.lehrjahr.setItemText(2, QCoreApplication.translate("MainWindow", u"3 LJ", None))

#if QT_CONFIG(tooltip)
        self.lehrjahr.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auswahl des Lehrjahres</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lbl_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.name.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Name des Auszubildenden </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Aus CSV Generieren", None))
#if QT_CONFIG(tooltip)
        self.csv_drop.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>CSV Datei aus von dem SuccessFactor hier hineinziehen</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.csv_drop.setText(QCoreApplication.translate("MainWindow", u"CSV Hier einf\u00fcgen", None))
#if QT_CONFIG(tooltip)
        self.gen_but.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Erstellt einen Ausbildungsnachweis basierend auf dem CSV File</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.gen_but.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.gen_but.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
        self.tmp_set_box.setTitle(QCoreApplication.translate("MainWindow", u"Vorlage Dokument", None))
        self.cb_vorlage_montag.setText(QCoreApplication.translate("MainWindow", u"Montag", None))
        self.cb_vorlage_dienstag.setText(QCoreApplication.translate("MainWindow", u"Dienstag", None))
        self.cb_vorlage_mittwoch.setText(QCoreApplication.translate("MainWindow", u"Mittwoch", None))
        self.cb_vorlage_freitag.setText(QCoreApplication.translate("MainWindow", u"Donnerstag", None))
        self.cb_vorlage_Freitag.setText(QCoreApplication.translate("MainWindow", u"Freitag", None))
        self.lbl_tmp_date.setText(QCoreApplication.translate("MainWindow", u"Monat/Jahr", None))
#if QT_CONFIG(tooltip)
        self.tmp_date.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auswahl des Monats und des Jahres f\u00fcr das die Vorlage erstellt werden soll</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tmp_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"MM.yyyy", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Berufsschultage:", None))
#if QT_CONFIG(tooltip)
        self.gen_but_tmp.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Erstellt eine Ausbildungs Nachweis Vorlage basierent auf dem Vorlage Datum</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.gen_but_tmp.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.gen_but_tmp.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
    # retranslateUi

