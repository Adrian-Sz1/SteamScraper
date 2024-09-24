import json
import csv
import yaml
import os
from bs4 import BeautifulSoup
import requests
import modules.helpers as helpers
import modules as modules
import modules.programsettings as ps
import logging
import modules.constants as c
import modules.enums.file_types as file_types

logger = logging.getLogger(__name__)

output_dict = {}  # username : error/success result


def validate_api_key(api_key: str):
    r = sendRequestWrapper('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+api_key+'&steamids=76561197960435530')
    if r.status_code == 200:
        logger.info('Steam API key is VALID')
    else:
        logger.info('Steam API key is INVALID')
    return r.status_code == 200


def start(api_key: str, usernames: str, folder_path: str, search_options: dict):
    logger.info('Scraping has started with the following attributes: usernames="' + usernames + '" folder_path="' + folder_path + '" search_options=' + helpers.dictToString(search_options, ', '))

    usernames = parseInput(usernames)
    ps.readSearchedUsersFile()
    output_dict.clear()

    for username in usernames:
        url = c.URL_PREFIX + username

        r = sendRequestWrapper(url)
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


def tryCreateEmptyOutputFile(steamId: str, folder_path: str, file_type: str):
    """
    Create a new empty file of a given file type. If file already exists in the path specified, the existing file is returned.
    """
    if not file_types.SupportedFileType.is_supported(file_type):
        logger.info(''.join([file_type,
                             ' is not a supported file type, file "',
                             steamId,
                             '_',
                             modules.currentDate,
                             '" will not be saved']))
        return None

    file_name = steamId + '_' + modules.currentDate + '.' + file_type

    file_dir = ''
    match ps.create_sub_folders:
        case True: file_dir = folder_path + '/' + file_type + '/' + steamId + '/'
        case False: file_dir = folder_path + '/' + file_type + '/'

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file = open(file_dir + file_name, "w")

    return file


def writeOutputFile(steamId: str, content, folder_path: str, file_type: str):
    file = tryCreateEmptyOutputFile(steamId, folder_path, file_type)
    logger.info('Writing to "' + file.name + '"')
    match file_type:
        case file_types.SupportedFileType.csv.name:
            generateCsvDataFile(file, content)
        case file_types.SupportedFileType.json.name:
            generateJsonDataFile(file, content)
        case file_types.SupportedFileType.yaml.name:
            generateYamlDataFile(file, content)


def remapOutputData(jsonData: dict):
    games_dict = jsonData['response']['games']

    total_playtime = 0
    total_playtime2weeks = 0

    # TODO: This is inefficient, most games will not have this field - this means tech debt :)
    for game in games_dict:

        total_playtime += game['playtime_forever']

        if 'playtime_2weeks' in game:
            total_playtime2weeks += game['playtime_2weeks']
        else:
            game['playtime_2weeks'] = 0

    output_template = {
        "game_count": jsonData['response']['game_count'],
        "total_playtime": total_playtime,
        "total_playtime2weeks": total_playtime2weeks,
        "games": games_dict
    }

    return output_template


def generateJsonDataFile(file, content):

    save_file_json = json.dumps(content, indent=2)

    file.write(save_file_json)

    file.close()

    logger.info('Json data file created for "' + file.name + '"')


def generateYamlDataFile(file, content):
    yaml.dump(content, file, allow_unicode=True)

    file.close()

    logger.info('Yaml data file created for "' + file.name + '"')


def generateCsvDataFile(file, content: dict):
    games = content['games']
    games1 = games[0].keys()
    with file as f:
        w = csv.DictWriter(f, games1)
        w.writeheader()
        for game in games:
            w.writerow(game)

    f.close()

    logger.info('Csv data file created for "' + file.name)

    return True


def scrapeGameData(api_key: str, steamId: str, folder_path: str):
    logger.info('Scraping game data for user ' + steamId)
    url = ''
    # Check if we are dealing with a vanity url or an actual steam id
    if steamId.isalnum() or not steamId.__len__() == 17:
        logger.info(steamId + ' is alphanumeric fetching steam64id...')
        if steamId not in ps.searched_users_dict:
            url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=' + api_key + '&vanityurl=' + steamId
            r = sendRequestWrapper(url)
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

    r = sendRequestWrapper(url)

    writeOutputFile(steamId, remapOutputData(r.json()), folder_path, ps.output_file_type)

# Get game names using appids https://store.steampowered.com/api/appdetails?appids=2630


def sendRequestWrapper(url: str):
    r = requests.get(url)

    url = url.replace(ps.steam_api_key, '[STEAM API KEY REDACTED]')

    logger.info(''.join(['Status code ', str(r.status_code), ' for request ', url]))

    return r
