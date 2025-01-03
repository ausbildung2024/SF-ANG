import configparser
import logging
import os
from pathlib import Path
from sysconfig import get_paths
from typing import Any, Dict, TypedDict
from src.ConfigData import settings

SEC = 'Settings'

class ConfigManager:

    def __init__(self, logger = None):
        self.config = None
        self.settings = settings
        self.load_ini()

    def load_ini(self):
        config_path = self.get_config_path()
        self.config = configparser.ConfigParser()
        self._ensure_path_exists(config_path.parent)

        if not config_path.exists():
            self.write_default_config()
        else:
            try:
                self.config.read(config_path)
                if self.config.has_section(SEC):
                    if self.config.has_option(SEC, 'name'):
                        self.set_name(self.config.get(SEC, 'name'))
                    if self.config.has_option(SEC,'year'):
                        self.set_year(self.config.get(SEC, 'year'))
                    if self.config.has_option(SEC,'default_hours'):
                        self.set_default_hours(self.config.get(SEC,'default_hours'))
            except Exception as e:
                pass

    def write_default_config(self):
        pass

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

    def set_ini_param(self, param, value):
        self.config.set(SEC, param, value)
        with open(self.get_config_path(), 'w') as file:
            self.config.write(file)

    def get_name(self):
        return self.get_personal()['name']

    def set_name(self, name):
        self.set_ini_param('name', name)
        self.settings['personal']['name'] = name

    def get_year(self):
        return self.get_personal()['year']

    def set_year(self, year):
        self.set_ini_param('year', year)
        self.settings['personal']['year'] = year

    def get_default_hours(self):
        return self.get_personal()['default_hours']

    def set_default_hours(self, default_hours):
        self.set_ini_param('default_hours', default_hours)
        self.settings['personal']['default_hours'] = default_hours

    def get_csv_path(self):
        return self.get_paths()['input_csv']

    def get_template_path(self):
        return self.get_paths()['template']

    def get_output_path(self):
        return self.get_paths()['output']

    def get_log_path(self):
        return self.get_paths()['log']

    def get_app_id(self):
        return self.get_app()['id']

    def get_labels(self):
        return self.settings['labels']

    def get_label(self,label):
        if label in self.get_labels():
            return self.get_labels()[label]
        return 'PLACEHOLDER'

    def get_filetypes(self):
        return self.settings['filetypes']

    def get_filetype(self,filetype):
        if filetype in self.get_filetypes():
            return self.get_filetypes()[filetype]
        return ''
