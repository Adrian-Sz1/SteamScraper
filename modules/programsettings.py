import json

#region settings
settingsPath = './settings.json'

output_folder_path = ''
output_file_type = ''
create_sub_folders = True
previous_parameters = ''
steam_api_key = ''
search_options = {}
#endregion


def writeSettings(outputFileType, outputFolderPath, createSubFolders, previousParameters, steamApiKey, searchOptions):
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

    settings_data_json = json.dumps(settings_data, indent=2)

    file = open(settingsPath, "w")

    file.write(settings_data_json)

    file.close()


def readSettings():
    global output_folder_path, output_file_type, create_sub_folders, previous_parameters, steam_api_key, search_options

    file = open(settingsPath, "r")
    settings_data = json.load(file)

    output_folder_path = settings_data['preferences']['output_folder_path']
    output_file_type = settings_data['preferences']['output_file_type']
    create_sub_folders = settings_data['preferences']['create_sub_folders']
    previous_parameters = settings_data['preferences']['previous_parameters']
    steam_api_key = settings_data['preferences']['steam_api_key']
    search_options = settings_data['preferences']['search_options']
