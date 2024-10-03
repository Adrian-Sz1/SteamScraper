import json
import logging

import modules.helpers.constants as constants
from modules.helpers.file_manager import FileManager

logger = logging.getLogger(__name__)

class SearchedUsersModel:
    def __init__(self, working_dir: str):
        self.working_dir = working_dir
        self.file_name = constants.SEARCHED_USERS_FILE_NAME

        self.searched_users_dict = {}

    def __get__(self, instance, owner):
        return self.searched_users_dict

    def load_searched_users(self):
        file = FileManager.load_file_in_dir(self.working_dir, self.file_name)

        if file is None:
            self.save_searched_users()
            file = FileManager.load_file_in_dir(self.working_dir, self.file_name)
        searched_users_data = json.load(file)

        self.searched_users_dict = searched_users_data

        file.close()
        logger.info(self.file_name + ' read in successfully "' + self.working_dir + self.file_name + '"')

    def save_searched_users(self):
        file = FileManager.create_file_in_dir(self.working_dir, self.file_name, True)

        searched_users_data_json = json.dumps(self.searched_users_dict, indent=2)

        file.write(searched_users_data_json)

        file.close()
