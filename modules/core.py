import json
import os
import time

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import modules.helpers as helpers
import modules as modules

URL_PREFIX = 'https://steamcommunity.com/id/'
URL_SUFFIX = '/games/?tab=all&sort=playtime'

API_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
API_URL_PREFIX = '&steamid='
API_URL_SUFFIX = '&format=json'

RESOLVE_VANITY_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key='
RESOLVE_VANITY_URL_SUFFIX = '&vanityurl='

#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version='128.0.6613.137').install()))

output_dict = {}  # username : error/success result


def __validateSteamId(steamId):
    """Checks whether the steamId leads to a valid url
    Returns game_list html div if website can be parsed correctly, otherwise returns None"""

    # TODO: Since we are trying to look for only a url and the div for game.ListRow
    #  static webpage way of scraping data using requests can be used to check if url is valid
    url = "https://steamcommunity.com/id/" + steamId + "/games/?tab=all&sort=playtime"

    #html = BeautifulSoup(driver.page_source, features='html.parser')
    #game_list_div = html.select("div.gameListRow")

    #if len(game_list_div) <= 0:
        #ConsoleMessages.ERRORMSG("SteamId not found or profile is private!", True)
        #return None

    #global currentUserName, currentSteamId
    #currentUserName = html.find('span', "profile_small_header_name").text
    #currentUserName = currentUserName.replace('\n', '')
    #currentUserName = currentUserName.replace('\t', '')
    #currentSteamId = steamId

    #ConsoleMessages.OKMSG('Found: [' + currentUserName + ']|[' + currentSteamId + ']', False)

    #return game_list_div


def validate_api_key(api_key: str):
    r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+api_key+'&steamids=76561197960435530')
    return r.status_code == 200


def start(api_key: str, usernames: str, folder_path: str):
    usernames = parseInput(usernames)

    output_dict.clear()

    for username in usernames:
        url = URL_PREFIX + username

        r = requests.get(url)
        html = BeautifulSoup(r.content, features='html.parser')

        if html.find(string='The specified profile could not be found.'):
            output_dict[username] = helpers.OutputUserStatus.NOT_FOUND.value

        else:
            output_dict[username] = helpers.OutputUserStatus.SUCCESSFUL.value
            scrapeGameData(api_key, username, folder_path)

    return parseDictToString(output_dict)


def parseDictToString(unparsedOutput: dict):
    output = ''

    for key in unparsedOutput:
        output += '[' + key + '] ' + unparsedOutput[key] + '\n'

    return output


def parseInput(input_usernames: str):
    return input_usernames.split('\n')


def generateJsonData():
    if len(modules.currentGameData) <= 0:
        ConsoleMessages.no_game_data_found()
        return False

    total_hours = float()
    for game in currentGameData[0]: total_hours += game[1]

    data = {
        'details': {
            'steam_id': currentSteamId,
            'username': currentUserName,
            'date_of_scrape': currentDate,
            'hours_on_record': round(total_hours, 2),
            'total_games': len(currentGameData[0])
        },
        'games': dict(currentGameData[0]),
    }
    global history
    history.append(currentSteamId + '_' + currentDate + '.json')

    return data

def convertToExcel():  # TODO: Refactor
    if len(currentGameData) <= 0:
        ConsoleMessages.no_game_data_found()
        return False

    # TODO: Create workbook if one doesn't exist already
    wb_name = ScrapeDataPath + "XLSX/" + GameDataScraper.applyFileName() + '.xlsx'
    wb = load_workbook(wb_name)
    ws = wb.active

    row = 2

    for game in currentGameData:
        ws['B' + str(row)] = game[0]
        ws['C' + str(row + 1)] = float(game[1])
        row += 1
    # ws.column_dimensions['C'].number_format = u'#,##0.00€'

    wb.save(wb_name)
    wb.close()
    return True

def generateJsonDataFile(steamId: str, jsonData, folder_path: str):
    file_name = steamId + '_' + modules.currentDate + '.json'
    file_dir = folder_path + '/Json/' + steamId+'/'

    # NOT FINISHED
    ###########################################
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        if not os.path.exists(file_dir + file_name):
            print('')  # Do nothing for now
    #    Menus.displayOptions(options)
    #    Menus.confirmPromptMenu()
    ###########################################

    save_file_json = json.dumps(jsonData, indent=2)

    file = open(file_dir + file_name, "w")

    file.write(save_file_json)

    file.close()
    return True

def scrapeGameData(api_key: str, steamId: str, folder_path: str):
    #currentGameData.clear()
    timeStart = time.perf_counter()

    url = ''
    # Check if we are dealing with a vanity url or an actual steam id
    if not steamId.isalnum() and not steamId.__len__() == 17:
        url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key='+api_key+'&vanityurl='+steamId
        r = requests.get(url)
        rjson = r.json()
        gg = rjson['response']
        steamId = gg['steamid']

    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + api_key + '&steamid=' + steamId + '&include_appinfo=false&include_played_free_games=true&format=json'

    r = requests.get(url)
    generateJsonDataFile(steamId, r.json(), folder_path)

# TODO Add a dict and save vanityURL resolved users i.e. Royal_Cabbage : 76561198049832868 to prevent unecessary calls for previously scraped users
# Get game names using appids https://store.steampowered.com/api/appdetails?appids=2630