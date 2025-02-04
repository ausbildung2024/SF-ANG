import configparser

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

