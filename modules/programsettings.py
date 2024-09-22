import json
import os

# region settings
settingsPath = ''
SETTINGS_FILE_NAME = 'settings.json'

APP_NAME = 'Steam User Scraper'
OS_USERNAME = ''

output_folder_path = ''
output_file_type = ''
create_sub_folders = True
previous_parameters = ''
steam_api_key = ''
search_options = {}


# endregion


def setUsernameOnOS():
    global OS_USERNAME
    if OS_USERNAME == '':
        OS_USERNAME = os.getenv("USERNAME")


def validateSettingsFileExists():
    global settingsPath
    setUsernameOnOS()
    settingsPath = 'C:/Users/' + OS_USERNAME + '/AppData/Roaming/' + APP_NAME
    return os.path.isfile(settingsPath + '/' + SETTINGS_FILE_NAME)


def createDefaultSettingsFile():
    if not os.path.exists(settingsPath):
        os.mkdir(settingsPath)
    settings_data = {
        "preferences": {
            "output_folder_path": settingsPath + '/' + 'data',
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
    writeJsonFile(settingsPath + '/' + SETTINGS_FILE_NAME, settings_data, 'x')


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

    writeJsonFile(settingsPath + '/' + SETTINGS_FILE_NAME, settings_data, 'w')


def writeJsonFile(path: str, content: dict, mode: str):
    settings_data_json = json.dumps(content, indent=2)

    file = open(path, mode)

    file.write(settings_data_json)

    file.close()


def readSettings():
    if not validateSettingsFileExists():
        createDefaultSettingsFile()

    global output_folder_path, output_file_type, create_sub_folders, previous_parameters, steam_api_key, search_options

    file = open(settingsPath + '/' + SETTINGS_FILE_NAME, "r")
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

