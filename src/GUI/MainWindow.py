import sys

from src.FileManagment.INIProcessor import IniLoader
from src.FileManagment.WeekDataProcessor import WeekDataProcessor
from src.FileManagment.WordProcessor import WordTemplate
from src.GUI.AutoGenerated.AG_MainWindow import Ui_MainWindow
from src.FileManagment.CSVProcessor import CSVProcessor

from src.Utils.CONSTANTS import *

class MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.csv_processor = CSVProcessor()
        self.ini = IniLoader()
        self.ini.load_ini()
        self.csv_path = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        
        #Verbinden des Buttons mit den Funktionen
        self.gen_but.pressed.connect(lambda: self.on_gen_but_pressed())
        self.gen_but_tmp.pressed.connect(lambda: self.on_gen_but_tmp_pressed())
        self.successfactor_but.pressed.connect(lambda: self.on_sf_but_pressed())
        self.appdata_but.pressed.connect(lambda: self.on_appdata_but_pressed())
        self.config_but.pressed.connect(lambda: self.on_config_but_pressed())
        self.save_but.pressed.connect(lambda: self.on_save_but_pressed())

        
        #Vorlage Datum
        self.set_temp_date(year=datetime.now().year,month=datetime.now().month)

        #Laden aus der INI
        self.set_name(self.ini.get_pers_name())

        self.set_lehrjahr(self.ini.get_pers_year())

        self.cb_vorlage_montag.setChecked(self.ini.get_tmp_day(0))
        self.cb_vorlage_dienstag.setChecked(self.ini.get_tmp_day(1))
        self.cb_vorlage_mittwoch.setChecked(self.ini.get_tmp_day(2))
        self.cb_vorlage_donnerstag.setChecked(self.ini.get_tmp_day(3))
        self.cb_vorlage_freitag.setChecked(self.ini.get_tmp_day(4))

        #Weiter Window Funktionen
        self.csv_drop.set_main_window(self)
        self.set_window_icon(MainWindow)

    def set_name(self,text):
        self.name.setText(text)
        self.name.repaint()

    def set_window_icon(self,MainWindow):
        app_icon = QtGui.QIcon()

        if getattr(sys, 'frozen', False):
            app_icon.addFile(str(os.path.join(sys._MEIPASS,PTH_ICN_S_EXE)), QtCore.QSize(16, 16))
            app_icon.addFile(str(os.path.join(sys._MEIPASS,PTH_ICN_L_EXE)), QtCore.QSize(32, 32))
        else:
            app_icon.addFile(PTH_ICN_S.as_posix(), QtCore.QSize(16, 16))
            app_icon.addFile(PTH_ICN_L.as_posix(), QtCore.QSize(32, 32))

        MainWindow.setWindowIcon(app_icon)

    def get_name(self):
        return self.name.text()

    def set_lehrjahr(self,lehrjahr):
        self.lehrjahr.setCurrentIndex(lehrjahr - 1)
        self.name.repaint()

    def get_lehrjahr(self):
        return self.lehrjahr.currentIndex() + 1

    def load_template(self):

        word_template = None

        if getattr(sys, 'frozen', False):
            word_template = WordTemplate(os.path.join(sys._MEIPASS,PTH_TMP_EXE))
        else:
            word_template = WordTemplate(Path(PTH_TMP))


        if word_template.document is None:  # Falls das Laden der Word-Vorlage fehlschlägt, wird eine Fehlermeldung angezeigt
            #self.show_error("Fehler beim Laden der Vorlage.")
            return
        return word_template

    def on_gen_but_pressed(self,date = None):
        #Überprüfung ob Einstellungen verändert wurden
        self.update_config()

        #Laden des Templates
        template = self.load_template()

        #Verarbeitung der Daten
        try:
            if self.csv_path is None and date is None:
                raise FileNotFoundError(ERR_CSV_NL)

            data = self.get_data()

            if date is None:
                self.csv_processor.load_csv(Path(self.csv_path))
                WeekDataProcessor(template, self.csv_processor).process_all_weeks(data)
            else:
                school = self.get_temp_week_data()
                WeekDataProcessor(template, self.csv_processor,school).process_all_empty_weeks(date,data, school)

            output_path = template.save_document(Path(PTH_OUT))
            #self.show_success("Dokument erfolgreich erstellt.")
            os.startfile(output_path)
        except Exception as e:
            emsg = str(e)
            create_error_dialog(emsg)
            pass


    def set_csv_path(self,param):
        param = param.replace('file:///','')
        if param.endswith(FILETYPE_CSV) and Path(param).exists():
            self.csv_path = param
            return True
        else:
            return False


    def get_data(self):
        return {
            'name' : self.get_name(),
            'year'  :self.get_lehrjahr(),
        }

    def update_config(self):
        self.ini.set_pers_name(self.get_name())
        self.ini.set_year(str(self.get_lehrjahr()))
        tmp_weeks = self.get_temp_week_data()
        for day in tmp_weeks:
            self.ini.set_tmp_day(WORK_DAYS.index(day),str(tmp_weeks[day]))
        self.ini.save_config()

    def on_sf_but_pressed(self):
        webbrowser.open(LNK_TP, new=0, autoraise=True)

    def on_appdata_but_pressed(self):
        os.startfile(PTH_APP_DATA)

    def on_config_but_pressed(self):
        os.startfile(PTH_CNFG)

    def on_gen_but_tmp_pressed(self):
        date = self.get_temp_date_dict()
        self.on_gen_but_pressed(date)

    def set_temp_date(self, year: int, month: int):
        self.tmp_date.setDate(QDate(year,month,1))

    def get_temp_date_dict(self):
        return { DADI_YEAR : self.tmp_date.date().year() , DADI_MONTH : self.tmp_date.date().month() }

    def get_temp_week_data(self):
        return {
            WORK_DAYS[0]: self.cb_vorlage_montag.isChecked(),
            WORK_DAYS[1]: self.cb_vorlage_dienstag.isChecked(),
            WORK_DAYS[2]: self.cb_vorlage_mittwoch.isChecked(),
            WORK_DAYS[3]: self.cb_vorlage_donnerstag.isChecked(),
            WORK_DAYS[4]: self.cb_vorlage_freitag.isChecked()
        }

    def on_save_but_pressed(self):
        self.update_config()
        create_success_dialog(SCC_STG_LO)