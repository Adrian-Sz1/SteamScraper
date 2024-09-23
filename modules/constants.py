# Name of the settings file where the user preferences are stored
SETTINGS_FILE_NAME = 'settings.json'
# Name of the searched users file where the previously searched users are stored
SEARCHED_USERS_NAME = 'searched_users.json'
# Name of the program
APP_NAME = 'Steam User Scraper'

URL_PREFIX = 'https://steamcommunity.com/id/'
URL_SUFFIX = '/games/?tab=all&sort=playtime'

API_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
API_URL_PREFIX = '&steamid='
API_URL_SUFFIX = '&format=json'

RESOLVE_VANITY_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key='
RESOLVE_VANITY_URL_SUFFIX = '&vanityurl='