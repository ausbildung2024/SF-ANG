import sys
from pathlib import Path
from docx import Document
from PySide6.QtCore import QDate
from PySide6 import QtGui, QtCore

import configparser
import pandas as pd
import webbrowser
import os

# Utils
from src.Utils.DateUtil import *
from src.Utils.FileUtil import *
from src.Utils.UiUtils import *

# App Informationen:
APP_NAME = 'SF-ANG'
APP_VERSION = '1.0.0'
APP_ID = APP_NAME + 'V' + APP_VERSION

# Allgemeine Informationen:
WORK_DAYS = ["MONTAG", "DIENSTAG", "MITTWOCH", "DONNERSTAG", "FREITAG"]
WORK_HOURS = 8

# Week Data Datensätze:
WDA_CON = 'Inhalt'
WDA_TYP = 'Art'

# Aktivitäten:
ACT_BS = 'Berufsschule'
ACT_BT = 'Betrieb'
ACT_NA = 'NA'
ACT_OT = 'Urlaub/Feiertag'

# CSV:
CSV_DIL = ';'

CSV_FLD_ACT = 'Tätigkeitsbeschreibung'
CSV_FLD_DAY = 'Tag'
CSV_FLD_CON = 'Beschreibung'
CSV_FLD_DAT = 'Datum'

CSV_FLDS = {CSV_FLD_DAT, CSV_FLD_DAY, CSV_FLD_ACT, CSV_FLD_CON}

CSV_ACTIVITY = {
    'NE-NICHT-PRÄMIENWIRKSAME AUSBILDUNG': 'Betrieb',  # Aktivitätstypen
    'AS-KRANKHEIT': 'Krank',
    'AH-URLAUB': 'Urlaub',
    'NA': 'Tätigkeit unbekannt! '
}

# File Arten:
FILETYPE_CSV = '.csv'
FILETYPE_WORD = '.docx'

# Error Nachrichten
ERR_CSV_NC = "Das erstellen eines CSV Loaders ist schiefgelaufen"
ERR_CSV_NL = "Das laden der CSV ist schiefgelaufen"
ERR_CSV_NV = 'Die CSV ist nicht vollständig! Es fehlen Folgende Zeilen: {}. Überprüfe ob die CSV die richtige Sprache hat'

# Success Nachrichten
SCC_CSV_LO = "File erfolgreich geladen!"
SCC_STG_LO = "Einstellungen gespeichert"

# WORD Spezifisches
WORD_NAME = 'Ausbildungsnachweis_{}.docx'
WORD_TIME = "%Y%m%d_%H%M%S"

# Date Dict
DADI_YEAR = 'year'
DADI_MONTH = 'month'

# INI Daten
SECTION_PERS = 'Persoenliches'
SECTION_GENR = 'Allgemeine Einstellungen'
SECTION_TEMP = 'Vorlagen Spezifische Einstellungen'
SECTION_CSVG = 'CSV Spezifische Einstellungen'

SETT_NAME = 'name'
SETT_YEAR = 'ausbildungsjahr'

# Pfade
APPDATA_PATH = Path(os.getenv('APPDATA', ''))
PTH_APP_DATA = Path(str(APPDATA_PATH / APP_NAME))
PTH_OUT = Path.home() / 'Documents'
PTH_TMP = Path.cwd() / 'res/template/month.docx'
PTH_TMP_EXE = 'month.docx'
PTH_CNFG = PTH_APP_DATA / 'config.ini'
PTH_LOG = Path(str(APPDATA_PATH / APP_NAME / 'logs'))
PTH_ICN_S = Path.cwd() / 'res/pictures/icon_16x.png'
PTH_ICN_L = Path.cwd() / 'res/pictures/icon_32x.png'
PTH_ICN_S_EXE = 'icon_16x.png'
PTH_ICN_L_EXE = 'icon_32x.png'

# Links
LNK_TP = 'https://portal.nagarro-es.com/ess/shells/abap/FioriLaunchpad.html#TIMEREPORTING_NAG-create?OnBehalfOf'
LNK_GH = 'https://github.com/ausbildung2024/SF-ANG'

#Standard Einstellungen
DSET_NAME = 'Gustav Gustavson'
DSET_YEAR = '1'
