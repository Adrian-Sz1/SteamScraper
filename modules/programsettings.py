import json
import os
import logging

logger = logging.getLogger(__name__)

# region settings
appdata_path = ''
SETTINGS_FILE_NAME = 'settings.json'
SEARCHED_USERS_NAME = 'searched_users.json'

APP_NAME = 'Steam User Scraper'
OS_USERNAME = ''

output_folder_path = ''
output_file_type = ''
create_sub_folders = True
previous_parameters = ''
steam_api_key = ''
search_options = {}

searched_users_dict = {}


# endregion


def setUsernameOnOS():
    global OS_USERNAME
    if OS_USERNAME == '':
        OS_USERNAME = os.getenv("USERNAME")


def getAppDataPath():
    setUsernameOnOS()
    return 'C:/Users/' + OS_USERNAME + '/AppData/Roaming/' + APP_NAME


def tryAppendNewUserToCache(display_name: str, steam_id: str):
    if str.isspace(display_name) or str.isspace(steam_id):
        return

    searched_users_dict[display_name] = steam_id
    writeJsonFile(appdata_path + '/' + SEARCHED_USERS_NAME, searched_users_dict, 'w')


def readSearchedUsersFile():
    if os.path.isfile(appdata_path + '/' + SEARCHED_USERS_NAME):
        global searched_users_dict
        file = open(appdata_path + '/' + SEARCHED_USERS_NAME, "r")
        searched_users_dict = json.load(file)


def validateSettingsFileExists():
    global appdata_path
    setUsernameOnOS()
    appdata_path = 'C:/Users/' + OS_USERNAME + '/AppData/Roaming/' + APP_NAME
    return os.path.isfile(appdata_path + '/' + SETTINGS_FILE_NAME)


def createDefaultSettingsFile():
    if not os.path.exists(appdata_path):
        logger.warning('Appdata directory does not exist')
        os.mkdir(appdata_path)
        logger.info('Appdata directory created')
    settings_data = {
        "preferences": {
            "output_folder_path": appdata_path + '/' + 'data',
            "output_file_type": 'json',
            "create_sub_folders": True,
            "previous_parameters": 'Usernames\nGo\nHere',
            "steam_api_key": '',
            "search_options": {
                "include_inventory": False,
                "include_games": True,
                "include_friends": False,
                "include_reviews": False,
                "include_profile_comments": False
            }
        }
    }
    logger.info('Creating default settings file in ' + '"' + appdata_path + '/' + SETTINGS_FILE_NAME + '')
    writeJsonFile(appdata_path + '/' + SETTINGS_FILE_NAME, settings_data, 'x')


def updateSettings(outputFileType, outputFolderPath, createSubFolders, previousParameters, steamApiKey, searchOptions):
    settings_data = {
        "preferences": {
            "output_folder_path": outputFolderPath,
            "output_file_type": outputFileType,
            "create_sub_folders": createSubFolders,
            "previous_parameters": previousParameters,
            "steam_api_key": steamApiKey,
            "search_options": {
                "include_inventory": searchOptions['include_inventory'],
                "include_games": searchOptions['include_games'],
                "include_friends": searchOptions['include_friends'],
                "include_reviews": searchOptions['include_reviews'],
                "include_profile_comments": searchOptions['include_profile_comments']
            }
        }
    }

    writeJsonFile(appdata_path + '/' + SETTINGS_FILE_NAME, settings_data, 'w')


def writeJsonFile(path: str, content: dict, mode: str):
    settings_data_json = json.dumps(content, indent=2)

    file = open(path, mode)

    file.write(settings_data_json)

    file.close()
    logger.info('Writing to file ' + '"' + path + '"]" in mode "' + mode + '"')


def updateSettingsFileKey(target_key: str, new_value):
    file = open(appdata_path + '/' + SETTINGS_FILE_NAME, "r")
    settings_data = json.load(file)

    file.close()

    if settings_data['preferences'].get(target_key) is None:
        return

    settings_data['preferences'][target_key] = new_value
    writeJsonFile(appdata_path + '/' + SETTINGS_FILE_NAME, settings_data, 'w')


def readSettings():
    if not validateSettingsFileExists():
        logger.warning('Settings file does not exist')
        createDefaultSettingsFile()

    global output_folder_path, output_file_type, create_sub_folders, previous_parameters, steam_api_key, search_options

    file = open(appdata_path + '/' + SETTINGS_FILE_NAME, "r")
    settings_data = json.load(file)

    if 'preferences' not in settings_data:
        return

    output_folder_path = settings_data['preferences']['output_folder_path']
    output_file_type = settings_data['preferences']['output_file_type']
    create_sub_folders = settings_data['preferences']['create_sub_folders']
    previous_parameters = settings_data['preferences']['previous_parameters']
    steam_api_key = settings_data['preferences']['steam_api_key']
    search_options = settings_data['preferences']['search_options']

    file.close()
    logger.info(SETTINGS_FILE_NAME + ' read in successfully "' + appdata_path + '/' + SETTINGS_FILE_NAME + '"')
