import configparser
from pathlib import Path
from src.SettingManagement.SettingsDict import settings

SETTINGS_SEC = 'SETTINGS'
PERSONAL_SEC = 'PERSONAL'
PATH_SEC = 'PATH'
ACTIVITY_SEC = 'ACTIVITY'


class IniLoader:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.config = config_manager.config
        self.settings = config_manager.settings

    def load_ini(self):
        config_path = self.config_manager.get_config_path()
        self.config = configparser.ConfigParser()
        self.config_manager._ensure_path_exists(config_path.parent)

        if not config_path.exists():
            self.config_manager.write_default_config()
        else:
            try:
                self.config.read(config_path)
                self.load_setting_section()
                self.load_personal_section()
                self.load_activity_section()
                self.load_path_section()
            except Exception as e:
                pass

    def load_setting_section(self):
        if not self.config.has_section(SETTINGS_SEC):
            self.config.add_section(SETTINGS_SEC)
        if self.config.has_option(SETTINGS_SEC, 'theme'):
            self.config_manager.set_theme(self.config.get(SETTINGS_SEC, 'theme'))

    def load_personal_section(self):
        if self.config.has_section(PERSONAL_SEC):
            if self.config.has_option(PERSONAL_SEC, 'name'):
                self.config_manager.set_name(self.config.get(PERSONAL_SEC, 'name'))
            if self.config.has_option(PERSONAL_SEC, 'year'):
                self.config_manager.set_year(self.config.get(PERSONAL_SEC, 'year'))
            if self.config.has_option(PERSONAL_SEC, 'default_hours'):
                self.config_manager.set_default_hours(self.config.get(PERSONAL_SEC, 'default_hours'))

    def load_activity_section(self):
        if self.config.has_section(ACTIVITY_SEC):
            pass

    def load_path_section(self):
        if self.config.has_section(PATH_SEC):
            pass


class ConfigManager:
    """
    Initialisiert den ConfigManager
    """

    def __init__(self, logger=None):
        self.config = configparser.ConfigParser()
        self.settings = settings
        self.ini_loader = IniLoader(self)
        self.ini_loader.load_ini()

    @staticmethod
    def _ensure_path_exists(path: Path):
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                pass

    def get_work_days(self):
        return self.settings['work_days']

    def get_activitys(self):
        return self.settings['activitys']

    def get_missing_day(self):
        return self.settings['missing_day']

    def get_messages(self):
        return self.settings['messages']

    def get_error_messages(self):
        return self.get_messages()['errors']

    def get_success_messages(self):
        return self.get_messages()['success']

    def get_warning_messages(self):
        return self.get_messages()['warnings']

    def get_info_messages(self):
        return self.get_messages()['infos']

    def get_personal(self):
        return self.settings['personal']

    def get_app(self):
        return self.settings['app']

    def get_app_name(self):
        return self.get_app()['name']

    def get_paths(self):
        return self.settings['paths']

    def get_app_icon(self, size):
        if size == 'large':
            return self.get_paths()['icon_large']
        else:
            return self.get_paths()['icon_small']

    def get_config_path(self):
        return self.get_paths()['config']

    def get_appdata_path(self):
        return self.get_paths()['appdata']

    def get_name(self):
        return self.get_personal()['name']

    def set_name(self, name):
        self.write_personal_param('name', name)
        self.settings['personal']['name'] = name

    def get_year(self):
        return self.get_personal()['year']

    def set_year(self, year):
        self.write_personal_param('year', year)
        self.settings['personal']['year'] = year

    def get_default_hours(self):
        return self.get_personal()['default_hours']

    def get_theme(self):
        return self.get_personal()['theme']

    def set_theme(self, theme):
        self.write_settings_param('theme', theme)
        self.settings['personal']['theme'] = theme

    def set_default_hours(self, default_hours):
        self.write_personal_param('default_hours', default_hours)
        self.settings['personal']['default_hours'] = default_hours

    def get_csv_path(self):
        return Path(self.get_paths()['input_csv']).as_posix()

    def get_template_path(self):
        return Path(self.get_paths()['template']).as_posix()

    def get_output_path(self):
        return Path(self.get_paths()['output']).as_posix()

    def get_log_path(self):
        return Path(self.get_paths()['log']).as_posix()

    def get_app_id(self):
        return self.get_app()['id']

    def get_labels(self):
        return self.settings['labels']

    def get_label(self, label):
        if label in self.get_labels():
            return self.get_labels()[label]
        return 'PLACEHOLDER'

    def get_filetypes(self):
        return self.settings['filetypes']

    def get_filetype(self, filetype):
        if filetype in self.get_filetypes():
            return self.get_filetypes()[filetype]
        return ''

    def get_csv_columns(self):
        return self.settings['csv_columns']

    def get_portal_link(self):
        return self.settings['links']['time_portal']

    ###########################################################################################
    # INI MANAGEMENT
    ###########################################################################################

    def write_default_config(self):
        self.write_settings_section()
        self.write_personal_section()
        self.write_activity_section()
        self.write_path_section()
        with open(self.get_config_path(), 'w') as file:
            self.config.write(file)

    """
    Schreibt die Dateien in den File
    """

    def write_file(self):
        with open(self.get_config_path(), 'w') as file:
            self.config.write(file)

    """Default Writer für die Jeweiligen Sektionen"""

    def write_settings_section(self):
        if not self.config.has_section(SETTINGS_SEC):
            self.config.add_section(SETTINGS_SEC)
        self.config.set(SETTINGS_SEC, 'theme', self.get_theme())

    def write_personal_section(self):
        self.config.add_section(PERSONAL_SEC)
        self.config.set(PERSONAL_SEC, 'name', self.get_name())
        self.config.set(PERSONAL_SEC, 'year', self.get_year())
        self.config.set(PERSONAL_SEC, 'default_hours', self.get_default_hours())

    def write_activity_section(self):
        pass

    def write_path_section(self):
        pass

    """Parameter Writer für die Jeweiligen Sektionen"""

    def write_settings_param(self, param, value):
        if not self.config.has_section(SETTINGS_SEC):
            self.config.add_section(SETTINGS_SEC)
        self.config.set(SETTINGS_SEC, param, value)
        self.write_file()

    def write_personal_param(self, param, value):
        if not self.config.has_section(PERSONAL_SEC):
            self.config.add_section(PERSONAL_SEC)
        self.config.set(PERSONAL_SEC, param, value)
        self.write_file()

    def write_activity_param(self, param, value):
        self.config.set(SETTINGS_SEC, param, value)
        self.write_file()

    def write_path_param(self, param, value):
        self.config.set(SETTINGS_SEC, param, value)
        self.write_file()
