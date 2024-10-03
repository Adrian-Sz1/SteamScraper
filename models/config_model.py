import json
import logging
import os

import modules.helpers.constants as constants
from modules.helpers.file_manager import FileManager

logger = logging.getLogger(__name__)

class ConfigModel:
    def __init__(self):
        self.file_name = constants.CONFIG_FILE_NAME
        self.default_config = {
            "app_name": 'Steam User Scraper',
            "root_directory": f'C:\\Users\\{os.getenv("USERNAME")}\\AppData\\Roaming\\', # App name is appended in root_directory getter,
            "build_version": 'v1.0.0',
            "copyright_license": 'None',
            "author": 'Adrian Sz'
        }
        self.config = {"configuration": self.default_config.copy()}

    def load_config(self):
        # TODO: Create a function from this. Lines 24-39, the code in settings_model.py and searched_users_model.py is the exact same
        file = FileManager.load_file_in_dir(self.root_directory, self.file_name)

        if file is None:
            self.save_config()
            file = FileManager.load_file_in_dir(self.root_directory, self.file_name)
        config_data = json.load(file)

        if 'configuration' not in config_data:
            logger.warning('Loaded preferences file is malformed, regenerating file...')
            self.save_config()

        for key, default_value in self.default_config.items():
            self.config['configuration'][key] = config_data['configuration'].get(key, default_value)

        file.close()
        logger.info(self.file_name + ' read in successfully "' + self.root_directory + self.file_name + '"')

    def save_config(self):

        file = FileManager.create_file_in_dir(self.root_directory, self.file_name, True)

        settings_data_json = json.dumps(self.config, indent=2)

        file.write(settings_data_json)

        file.close()

    @property
    def app_name(self):
        return self.config['configuration'].get('app_name', self.default_config['app_name'])

    @app_name.setter
    def app_name(self, value):
        self.config['configuration']['app_name'] = value

    @property
    def root_directory(self):
        return f"{self.config['configuration'].get('root_directory', self.default_config['root_directory'])}{self.app_name}"

    @root_directory.setter
    def root_directory(self, value):
        self.config['configuration']['root_directory'] = value

    @property
    def build_version(self):
        return self.config['configuration'].get('build_version', self.default_config['build_version'])

    @build_version.setter
    def build_version(self, value):
        self.config['configuration']['build_version'] = value

    @property
    def copyright_license(self):
        return self.config['configuration'].get('copyright_license', self.default_config['copyright_license'])

    @copyright_license.setter
    def copyright_license(self, value):
        self.config['configuration']['copyright_license'] = value

    @property
    def author(self):
        return self.config['configuration'].get('author', self.default_config['author'])

    @author.setter
    def author(self, value):
        self.config['configuration']['author'] = value
