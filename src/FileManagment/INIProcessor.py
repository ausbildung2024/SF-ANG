from src.Utils.CONSTANTS import *

class IniLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()

    """
    Lädt die Ini Datei.
    """
    def load_ini(self):
        self.config = configparser.ConfigParser()
        is_folder_valid(PTH_CNFG.parent)

        if not PTH_CNFG.exists():
            self.write_default_config()
        else:
            try:
                self.config.read(PTH_CNFG)
                self.load_general_section()
                self.load_personal_section()
            except Exception as e:
                pass

    def write_default_config(self):
        self.write_general_section()
        self.write_personal_section()
        self.write_template_section()
        self.write_csv_section()
        self.save_config()

    def save_config(self):
        with open(PTH_CNFG, 'w') as file:
            self.config.write(file)

    def write_general_section(self):
        if not self.config.has_section(SECTION_GENR):
            self.config.add_section(SECTION_GENR)


    def write_personal_section(self):
        if not self.config.has_section(SECTION_PERS):
            self.config.add_section(SECTION_PERS)
            self.config.set(SECTION_PERS, 'name', DSET_NAME)
            self.config.set(SECTION_PERS, 'year', DSET_YEAR)

    def write_template_section(self):
        if not self.config.has_section(SECTION_TEMP):
            self.config.add_section(SECTION_TEMP)
            self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[0]}', 'False')
            self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[1]}', 'False')
            self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[2]}', 'False')
            self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[3]}', 'False')
            self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[4]}', 'False')

    def write_csv_section(self):
        if not self.config.has_section(SECTION_CSVG):
            self.config.add_section(SECTION_CSVG)

    def load_general_section(self):
        if not self.config.has_section(SECTION_GENR):
            self.config.add_section(SECTION_GENR)

    def load_personal_section(self):
        pass

    def load_template_section(self):
        pass


    def set_section(self,section):
        if not self.config.has_section(section):
            self.config.add_section(section)

    """
    TODO
    """
    def set_tmp_day(self,day,value):
        self.set_section(SECTION_TEMP)
        self.config.set(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[day]}', value)

    """
    TODO
    """
    def get_tmp_day(self,day):
        if self.config.has_option(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[day]}'):
            return True if self.config.get(SECTION_TEMP, f'{ACT_BS}_{WORK_DAYS[day]}') == 'True' else False
        else:
            return False

    """
    Setzt das Ausbildungsjahr im Azubi Abschnitt
    """
    def set_year(self,year):
        self.set_section(SECTION_PERS)
        self.config.set(SECTION_PERS,SETT_YEAR,year)

    """
    Holt sich das Ausbildungsjahr des Azubis aus den Personal Abschnitt, wenn kein Jahr vorhanden ist, wird das default jahr genommen
    """
    def get_pers_year(self):
        if self.config.has_option(SECTION_PERS, SETT_YEAR):
            return int(self.config.get(SECTION_PERS, SETT_YEAR))
        else:
            return int(DSET_YEAR)

    """
    Setzt den Namen des Azubis im Personal Abschnitt
    """
    def set_pers_name(self,name):
        self.set_section(SECTION_PERS)
        self.config.set(SECTION_PERS,SETT_NAME, name)

    """
    Holt sich den Namen des Azubis aus den Personal Abschnitt, wenn kein Name vorhanden ist, wird der default name genommen
    """
    def get_pers_name(self):
        if self.config.has_option(SECTION_PERS, SETT_NAME):
            return self.config.get(SECTION_PERS, SETT_NAME)
        else:
            return DSET_NAME