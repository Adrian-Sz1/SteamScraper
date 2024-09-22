import json
import os
import time
from bs4 import BeautifulSoup
import requests
import modules.helpers as helpers
import modules as modules
import modules.programsettings as ps
import logging

logger = logging.getLogger(__name__)

output_dict = {}  # username : error/success result


def validate_api_key(api_key: str):
    r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+api_key+'&steamids=76561197960435530')

    if r.status_code == 200:
        logger.info('Steam API key is VALID')
    else:
        logger.info('Steam API key is INVALID')
    return r.status_code == 200


def start(api_key: str, usernames: str, folder_path: str, search_options: dict):
    logger.info('Scraping has started with the following attributes: usernames="' + usernames + '" folder_path="' + folder_path + '" search_options=')

    usernames = parseInput(usernames)
    ps.readSearchedUsersFile()
    output_dict.clear()

    for username in usernames:
        url = helpers.URL_PREFIX + username

        r = requests.get(url)
        html = BeautifulSoup(r.content, features='html.parser')

        if html.find(string='The specified profile could not be found.'):
            logger.info('User "' + username + '" could not be found')

            output_dict[username] = helpers.OutputUserStatus.NOT_FOUND.value
            continue

        output_dict[username] = helpers.OutputUserStatus.SUCCESSFUL.value

        if search_options['include_inventory']:
            print('include_inventory')
        if search_options['include_games']:
            scrapeGameData(api_key, username, folder_path)
        if search_options['include_friends']:
            print('include_friends')
        if search_options['include_reviews']:
            print('include_reviews')
        if search_options['include_profile_comments']:
            print('include_profile_comments')


    return parseDictToString(output_dict)


def parseDictToString(unparsedOutput: dict):
    output = ''

    for key in unparsedOutput:
        output += '[' + key + '] ' + unparsedOutput[key] + '\n'

    return output


def parseInput(input_usernames: str):
    return input_usernames.split(',')


# def generateJsonData():
#     if len(modules.currentGameData) <= 0:
#         ConsoleMessages.no_game_data_found()
#         return False
#
#     total_hours = float()
#     for game in currentGameData[0]: total_hours += game[1]
#
#     data = {
#         'details': {
#             'steam_id': currentSteamId,
#             'username': currentUserName,
#             'date_of_scrape': currentDate,
#             'hours_on_record': round(total_hours, 2),
#             'total_games': len(currentGameData[0])
#         },
#         'games': dict(currentGameData[0]),
#     }
#     global history
#     history.append(currentSteamId + '_' + currentDate + '.json')
#
#     return data
#
# def convertToExcel():  # TODO: Refactor
#     if len(currentGameData) <= 0:
#         ConsoleMessages.no_game_data_found()
#         return False
#
#     # TODO: Create workbook if one doesn't exist already
#     wb_name = ScrapeDataPath + "XLSX/" + GameDataScraper.applyFileName() + '.xlsx'
#     wb = load_workbook(wb_name)
#     ws = wb.active
#
#     row = 2
#
#     for game in currentGameData:
#         ws['B' + str(row)] = game[0]
#         ws['C' + str(row + 1)] = float(game[1])
#         row += 1
#     # ws.column_dimensions['C'].number_format = u'#,##0.00€'
#
#     wb.save(wb_name)
#     wb.close()
#     return True

def generateJsonDataFile(steamId: str, jsonData, folder_path: str):
    file_name = steamId + '_' + modules.currentDate + '.json'
    if ps.create_sub_folders:
        file_dir = folder_path + '/Json/' + steamId+'/'
    else:
        file_dir = folder_path + '/Json/'

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    #    if not os.path.exists(file_dir + file_name):
    #        print('')  # Do nothing for now
    #    Menus.displayOptions(options)
    #    Menus.confirmPromptMenu()
    ###########################################

    save_file_json = json.dumps(jsonData, indent=2)

    file = open(file_dir + file_name, "w")

    file.write(save_file_json)

    file.close()

    logger.info('Json data file created for ' + steamId + ' in "' + folder_path + '"')

    return True


def scrapeGameData(api_key: str, steamId: str, folder_path: str):
    logger.info('Scraping game data for user ' + steamId)
    url = ''
    # Check if we are dealing with a vanity url or an actual steam id
    if steamId.isalnum() or not steamId.__len__() == 17:
        logger.info(steamId + ' is alphanumeric fetching steam64id...')
        if steamId not in ps.searched_users_dict:
            url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=' + api_key + '&vanityurl=' + steamId
            r = requests.get(url)
            rjson = r.json()
            gg = rjson['response']

            ps.tryAppendNewUserToCache(steamId, gg['steamid'])

            steamId = gg['steamid']
            logger.info(steamId + ' fetched from Steam API')

        else:
            logger.info(steamId + ' found in search history')
            steamId = ps.searched_users_dict[steamId]


    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + api_key + '&steamid=' + steamId + '&include_appinfo=false&include_played_free_games=true&format=json'
    logger.info('Sending Owned Games request for user with id "' + steamId + '"')

    r = requests.get(url)

    logger.info('Owned Games status code=' + str(r.status_code))

    generateJsonDataFile(steamId, r.json(), folder_path)

# Get game names using appids https://store.steampowered.com/api/appdetails?appids=2630