import configparser
import logging
import os
from pathlib import Path
from typing import Any, Dict, TypedDict
from ConfigData import days, settings, activitys, missing_day, messages, app

class ConfigManager:

    def __init__(self, messages=messages, app=app, missing_day=missing_day, activitys=activitys, settings=settings, days=days):
        self.messages = messages
        self.app = app
        self.missing_day = missing_day
        self.activitys = activitys
        self.settings = settings
        self.days = days

