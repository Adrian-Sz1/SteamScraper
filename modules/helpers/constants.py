import os

# Name of the settings file where the user preferences are stored
SETTINGS_FILE_NAME = 'preferences.json'
CONFIG_FILE_NAME = 'app_config.json'

# Name of the searched users file where the previously searched users are stored if using their vanity id
SEARCHED_USERS_FILE_NAME = 'searched_users.json'

# Name of the searched users file where the previously searched users are stored
SEARCHED_USERS_NAME = 'searched_users.json'
# Name of the program
APP_NAME = 'Steam User Scraper'

VANITY_URL_PREFIX = 'https://steamcommunity.com/id/'
STEAM64ID_URL_PREFIX = 'https://steamcommunity.com/profiles/'

URL_SUFFIX = '/games/?tab=all&sort=playtime'

API_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
API_URL_PREFIX = '&steamid='
API_URL_SUFFIX = '&format=json'

RESOLVE_VANITY_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key='
RESOLVE_VANITY_URL_SUFFIX = '&vanityurl='


DEFAULT_WORKING_DIR = f'C:\\Users\\{os.getenv("USERNAME")}\\AppData\\Roaming\\{APP_NAME}\\'
