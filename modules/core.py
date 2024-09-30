from bs4 import BeautifulSoup
import modules.helpers as helpers
import modules.programsettings as ps
import logging
import modules.constants as c
import modules.enums.file_types as file_types
import modules.file_exporters as file_exporters
from modules.api_handler import sendRequestWrapper, resolve_vanity_url, get_owned_games
import modules.file_manager as file_manager

logger = logging.getLogger(__name__)

output_dict = {}  # username : error/success result


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

    return output_dict


def parseInput(input_usernames: str):
    return input_usernames.split(',')


def writeOutputFile(steamId: str, content, folder_path: str, file_type: str):
    file_name = file_manager.construct_default_file_user_name(steam_id=steamId, file_type=file_type)

    if ps.create_sub_folders:
        file_manager.construct_file_dir_user_sub_folders(folder_path, file_type, steamId)
    else:
        file_manager.construct_file_dir_default_path(folder_path, file_type)

    file = file_manager.create_file_in_dir(folder_path, file_name)
    logger.info('Writing to "' + file.name + '"')
    match file_type:
        case file_types.SupportedFileType.csv.name:
            file_exporters.generateCsvDataFile(file, content)
        case file_types.SupportedFileType.json.name:
            file_exporters.generateJsonDataFile(file, content)
        case file_types.SupportedFileType.yaml.name:
            file_exporters.generateYamlDataFile(file, content)


def remapOutputData(jsonData: dict):
    games_dict = jsonData['games']

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
        "game_count": jsonData['game_count'],
        "total_playtime": total_playtime,
        "total_playtime2weeks": total_playtime2weeks,
        "games": games_dict
    }

    return output_template


def scrapeGameData(api_key: str, steamId: str, folder_path: str):
    username = steamId
    logger.info('Scraping game data for user ' + steamId)

    # Check if we are dealing with a vanity url or an actual steam id
    if steamId.isalnum() or not steamId.__len__() == 17:
        if steamId not in ps.searched_users_dict:
            logger.info(username + ' fetching steam64id...')
            steamId = resolve_vanity_url(api_key=api_key, vanity_url_name=steamId)

            if steamId is None:
                logger.info('Steam id is empty, aborting...')
                return

            ps.tryAppendNewUserToCache(vanity_url_name=username, steam_id=steamId)
        else:
            logger.info(steamId + ' found in search history')
            steamId = ps.searched_users_dict[steamId]

    game_list = get_owned_games(api_key=api_key, steam64_id=steamId)

    if game_list is None:
        output_dict[username] = helpers.OutputUserStatus.ACCOUNT_PRIVATE.value
        return

    writeOutputFile(steamId, remapOutputData(game_list), folder_path, ps.output_file_type)
    return



# Get game names using appids https://store.steampowered.com/api/appdetails?appids=2630



