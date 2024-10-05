import json
import logging
import os.path

import PySimpleGUI as sg
from bs4 import BeautifulSoup

import modules.helpers.constants as c
from models.api_handler import SteamAPI
from models.config_model import ConfigModel
from models.searched_users_model import SearchedUsersModel
from models.settings_model import SettingsModel
from modules import helpers, currentDate
from modules.enums import file_types
from modules.helpers.common import validate_steam64id_format, remap_output_game_data
from modules.helpers.file_exporters import FileExporters
from modules.helpers.file_manager import FileManager
from views.gui import create_window

logger = logging.getLogger(__name__)

class CoreViewModel:
    def __init__(self, config_model: ConfigModel):
        self.config = config_model

        self.settings = SettingsModel(self.config.root_directory)
        self.searched_users = SearchedUsersModel(self.config.root_directory)
        self.searched_users.load_searched_users()
        self.settings.load_settings()

        self.api = SteamAPI(self.settings.steam_api_key)

        self.ui_window = create_window(self.settings.output_folder_path,
                                       self.settings.output_file_type,
                                       self.settings.create_sub_folders,
                                       self.settings.overwrite_enabled,
                                       self.settings.previous_parameters,
                                       self.settings.steam_api_key,
                                       self.settings.search_options)
        self.peek_enabled = False
        self.output_info_dict = {}


    def try_store_steam64id_from_vanity_id(self, input_id: str):
        # Check if we are dealing with a vanity url or an actual steam id
        if not validate_steam64id_format(input_id):
            if input_id not in self.searched_users.searched_users_dict:
                logger.info(input_id + ' fetching steam64id...')
                steam64id = SteamAPI.resolve_vanity_url(self.api, vanity_url_name=input_id)

                if steam64id is None:
                    logger.info(f"Steam64id for '{input_id}' could not be found")
                    return

                self.searched_users.searched_users_dict[input_id] = steam64id
            else:
                steam64id = self.searched_users.searched_users_dict[input_id]
                logger.info(f"Found matching steam64id for user '{input_id}' - '{steam64id}'")


    # TODO: Split this in to functions - it's too big and doesn't adhere to single responsibility principle
    def scrape_game_data(self, steam64id: str):
        username = steam64id
        logger.info('Scraping game data for user ' + steam64id)

        game_list = SteamAPI.get_owned_games(self.api, steam64id=steam64id)

        if game_list is None:
            self.output_info_dict[username] = helpers.common.OutputUserStatus.ACCOUNT_PRIVATE.value
            return

        game_list = remap_output_game_data(game_list)

        # e.g. ../Steam User Scraper/data/json/username/username_todaysdate.json
        # or ../Steam User Scraper/data/json/username_todaysdate.json

        if self.settings.create_sub_folders:
            target_dir = os.path.join(self.settings.output_folder_path,
                                      self.settings.output_file_type,
                                      username)
        else:
            target_dir = os.path.join(self.settings.output_folder_path,
                                      self.settings.output_file_type)


        full_file_name = f"{username}_{currentDate}.{self.settings.output_file_type}"

        file = FileManager.create_file_in_dir(working_dir=str(target_dir), file_name=full_file_name)

        match self.settings.output_file_type:
            case file_types.SupportedFileType.csv.name:
                FileExporters.generate_csv_data_file(file, game_list)
            case file_types.SupportedFileType.json.name:
                FileExporters.generate_json_data_file(file, game_list)
            case file_types.SupportedFileType.yaml.name:
                FileExporters.generate_yaml_data_file(file, game_list)

        return

    def run(self):
        settings_events_to_update = {
            '-OPTION MENU-',
            'output_folder_path',
            'user_sub_folder',
            'parameters_multiline',
            'steam_api_key',
            'inventory_checkbox',
            'games_checkbox',
            'friends_checkbox',
            'reviews_checkbox',
            'profile_comments_checkbox',
            'overwrite_enabled'
        }

        while True:
            event, values = self.ui_window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks exit
                break
            if event == 'save_button':
                self.settings.output_file_type = self.ui_window['-OPTION MENU-'].Get()
                self.settings.output_folder_path = self.ui_window['output_folder_path'].Get()
                self.settings.create_sub_folders = self.ui_window['user_sub_folder'].Get()
                self.settings.previous_parameters = self.ui_window['parameters_multiline'].Get()
                self.settings.overwrite_enabled = self.ui_window['overwrite_enabled'].Get()
                self.settings.steam_api_key = self.ui_window['steam_api_key'].Get()

                self.api.api_key = self.settings.steam_api_key

                result_output = self.ui_window['preferences_info_text']
                result_output.Update(text_color='green')
                result_output.Update('Changes saved')

                self.ui_window['save_button'].Update(visible=False)

                search_options = {
                    "include_inventory": self.ui_window['inventory_checkbox'].Get(),
                    "include_games": self.ui_window['games_checkbox'].Get(),
                    "include_friends": self.ui_window['friends_checkbox'].Get(),
                    "include_reviews": self.ui_window['reviews_checkbox'].Get(),
                    "include_profile_comments": self.ui_window['profile_comments_checkbox'].Get()
                }
                self.settings.search_options = search_options
                self.settings.save_settings()

            elif event in settings_events_to_update:
                self.ui_window['preferences_info_text'].Update(text_color='orange')
                self.ui_window['preferences_info_text'].Update('Unsaved Changes')
                self.ui_window['save_button'].Update(visible=True)

            if event == 'Start':
                self.settings.previous_parameters = self.ui_window['parameters_multiline'].get()

                self.start()

                self.ui_window['result_output'].Update(value=json.dumps(self.output_info_dict))

            if event == 'peek_key':
                self.peek_enabled = not self.peek_enabled
                if self.peek_enabled:
                    self.ui_window['steam_api_key'].update(password_char='')
                    self.ui_window['peek_key'].update("Hide")
                else:
                    self.ui_window['steam_api_key'].update(password_char='*')
                    self.ui_window['peek_key'].update("Show")

            if event == 'validate_api_key':
                api_test_result_element = self.ui_window['api_key_test_result']
                if self.api.validate_api_key(self.ui_window['steam_api_key'].Get()):
                    api_test_result_element.Update(text_color='green', value='OK')
                else:
                    api_test_result_element.Update(text_color='red', value='NOT OK')

        self.ui_window.close()

    def start(self):
        usernames = self.settings.previous_parameters.split(',')

        logger.info(f"Scraping has started with the following attributes: "
                    f"usernames='{usernames}' "
                    f"folder_path='{self.settings.output_folder_path}' "
                    f"search_options='{json.dumps(self.settings.search_options)}")

        self.output_info_dict.clear()

        if not SteamAPI.validate_steam_api_key_format(self.api.api_key) or not self.api.validate_api_key(self.api.api_key):
            logger.info(f"'Start' operation aborted")

            self.output_info_dict['INVALID API ERROR'] = 'The provided api key is not valid'
            return

        # TODO: Also check the viability of converting vanity urls here and using just steam64ids from this point onwards (could involve swapping searched_users dict's keys with values)
        for username in usernames:
            if helpers.common.validate_steam64id_format(username):
                if not self.check_user_profile_exists(c.STEAM64ID_URL_PREFIX, username):
                    continue
                steam_id = username
            else:
                if not self.check_user_profile_exists(c.VANITY_URL_PREFIX, username):
                    continue
                self.try_store_steam64id_from_vanity_id(username)
                steam_id = self.searched_users.searched_users_dict[username]

            # TODO: For now anytime a user is found, the output should be successful, this will be more robust with future feature implementations
            self.output_info_dict[username] = helpers.common.OutputUserStatus.SUCCESSFUL.value

            if self.settings.search_options['include_inventory']:
                print('include_inventory')
            if self.settings.search_options['include_games']:
                self.scrape_game_data(steam_id)
            if self.settings.search_options['include_friends']:
                print('include_friends')
            if self.settings.search_options['include_reviews']:
                print('include_reviews')
            if self.settings.search_options['include_profile_comments']:
                print('include_profile_comments')

    def check_user_profile_exists(self, url: str, username: str):
        r = self.api.send_request_wrapper(f"{url}{username}")
        html = BeautifulSoup(r.content, features='html.parser')
        # TODO: As this is html we are accessing there is a likelihood that if a profile has the text below, the program will classify it as non-existent
        # Best course of action would be to either look for something which cannot be altered by a user, or do an api call to steam
        if html.find(string='The specified profile could not be found.'):
            logger.info('User "' + username + '" could not be found')
            self.output_info_dict[username] = helpers.common.OutputUserStatus.NOT_FOUND.value
            return False
        return True
