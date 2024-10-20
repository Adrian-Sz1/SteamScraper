import json
import logging
import os

from PySide6.QtCore import QObject

import modules.helpers.constants as constants
from modules.helpers.file_manager import FileManager

logger = logging.getLogger(__name__)


class ConfigModel(QObject):
    def __init__(self):
        super(ConfigModel, self).__init__()
        self.file_name = constants.CONFIG_FILE_NAME
        self.default_config = {
            "app_name": 'Steam User Scraper',
            "root_directory": f'C:\\Users\\{os.getenv("USERNAME")}\\AppData\\Roaming\\', # App name is appended in root_directory getter,
            "build_version": 'v0.4.0',
            "copyright_license": 'None',
            "author": 'Adrian Sz',
            "default_font": 'Segoe UI Variable Small Semibol'
        }
        self.config = {"configuration": self.default_config.copy()}

    def load_config(self):
        file = FileManager.load_file_in_dir(self.default_config['root_directory'], self.file_name)

        if file is None:
            self.save_config()
            file = FileManager.load_file_in_dir(self.default_config['root_directory'], self.file_name)
        config_data = json.load(file)

        if 'configuration' not in config_data:
            logger.warning('Loaded preferences file is malformed, regenerating file...')
            self.save_config()

        for key, default_value in self.default_config.items():
            self.config['configuration'][key] = config_data['configuration'].get(key, default_value)

        file.close()
        logger.info(self.file_name + ' read in successfully "' + self.default_config['root_directory'] + self.file_name + '"')

    def save_config(self):
        file = FileManager.create_file_in_dir(self.default_config['root_directory'], self.file_name, True)
        settings_data_json = json.dumps(self.config, indent=2)
        file.write(settings_data_json)
        file.close()

    @property
    def app_name(self):
        """Get the application name from the configuration."""
        return self.config['configuration'].get('app_name', self.default_config['app_name'])

    @property
    def root_directory(self):
        """Get the root directory from the configuration, appending the app name."""
        return f"{self.config['configuration'].get('root_directory', self.default_config['root_directory'])}{self.app_name}"

    @property
    def build_version(self):
        """Get the build version from the configuration."""
        return self.config['configuration'].get('build_version', self.default_config['build_version'])

    @property
    def copyright_license(self):
        """Get the copyright license from the configuration."""
        return self.config['configuration'].get('copyright_license', self.default_config['copyright_license'])

    @property
    def author(self):
        """Get the author from the configuration."""
        return self.config['configuration'].get('author', self.default_config['author'])
    
    @property
    def font(self):
        """Get the font from the configuration."""
        return self.config['configuration'].get('default_font', self.default_config['default_font'])