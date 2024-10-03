import json
import logging

import modules.helpers.constants as constants
from modules.helpers.file_manager import FileManager

logger = logging.getLogger(__name__)

class SettingsModel:
    def __init__(self, working_dir: str):
        self.working_dir = working_dir
        self.file_name = constants.SETTINGS_FILE_NAME
        self.default_preferences = {
            "output_folder_path": self.working_dir + 'data/',
            "output_file_type": 'json',
            "create_sub_folders": True,
            "overwrite_enabled": True,
            "previous_parameters": 'Usernames,Go,Here',
            "steam_api_key": 'Api key goes here...',
            "search_options": {
                "include_inventory": False,
                "include_games": True,
                "include_friends": False,
                "include_reviews": False,
                "include_profile_comments": False
            }
        }
        self.preferences = {"preferences": self.default_preferences.copy()}

    def load_settings(self):
        file = FileManager.load_file_in_dir(self.working_dir, self.file_name)

        if file is None:
            self.save_settings()
            file = FileManager.load_file_in_dir(self.working_dir, self.file_name)
        settings_data = json.load(file)

        if 'preferences' not in settings_data:
            logger.warning('Loaded preferences file is malformed, regenerating file...')
            self.save_settings()

        for key, default_value in self.default_preferences.items():
            self.preferences['preferences'][key] = settings_data['preferences'].get(key, default_value)

        file.close()
        logger.info(self.file_name + ' read in successfully "' + self.working_dir + self.file_name + '"')

    def save_settings(self):
        file = FileManager.create_file_in_dir(self.working_dir, self.file_name, True)

        settings_data_json = json.dumps(self.preferences, indent=2)

        file.write(settings_data_json)

        file.close()

    @property
    def output_folder_path(self):
        return self.preferences['preferences'].get('output_folder_path', self.default_preferences['output_folder_path'])

    @output_folder_path.setter
    def output_folder_path(self, value):
        self.preferences['preferences']['output_folder_path'] = value

    @property
    def output_file_type(self):
        return self.preferences['preferences'].get('output_file_type', self.default_preferences['output_file_type'])

    @output_file_type.setter
    def output_file_type(self, value):
        self.preferences['preferences']['output_file_type'] = value

    @property
    def create_sub_folders(self):
        return self.preferences['preferences'].get('create_sub_folders', self.default_preferences['create_sub_folders'])

    @create_sub_folders.setter
    def create_sub_folders(self, value):
        self.preferences['preferences']['create_sub_folders'] = value

    @property
    def overwrite_enabled(self):
        return self.preferences['preferences'].get('overwrite_enabled', self.default_preferences['overwrite_enabled'])

    @overwrite_enabled.setter
    def overwrite_enabled(self, value):
        self.preferences['preferences']['overwrite_enabled'] = value

    @property
    def previous_parameters(self):
        return self.preferences['preferences'].get('previous_parameters', self.default_preferences['previous_parameters'])

    @previous_parameters.setter
    def previous_parameters(self, value):
        self.preferences['preferences']['previous_parameters'] = value

    @property
    def steam_api_key(self):
        return self.preferences['preferences'].get('steam_api_key', self.default_preferences['steam_api_key'])

    @steam_api_key.setter
    def steam_api_key(self, value):
        self.preferences['preferences']['steam_api_key'] = value

    @property
    def search_options(self):
        return self.preferences['preferences'].get('search_options', self.default_preferences['search_options'])

    @search_options.setter
    def search_options(self, value):
        self.preferences['preferences']['search_options'] = value