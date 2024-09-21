from enum import Enum

URL_PREFIX = 'https://steamcommunity.com/id/'
URL_SUFFIX = '/games/?tab=all&sort=playtime'

API_BASE_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
API_URL_PREFIX = '&steamid='
API_URL_SUFFIX = '&format=json'

RESOLVE_VANITY_URL = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key='
RESOLVE_VANITY_URL_SUFFIX = '&vanityurl='


class SupportedFileType(Enum):
    xlsx = 1
    csv = 2
    json = 3
    raw = 4


class OutputUserStatus(Enum):
    NOT_FOUND = 'User not found'
    ACCOUNT_PRIVATE = 'Account is private'
    YOU_MUST_BE_LOGGED_IN = 'Content cannot be accessed without login'
    UNEXPECTED_ERROR = 'Unexpected error has occurred'
    SUCCESSFUL = 'Success'


class ConsoleMessages:
    colours = {
        'HEADER': '\033[95m',
        'OKBLUE': '\033[94m',
        'INFOCYAN': '\033[96m',
        'INFOMAGENTA': '\033[35m',
        'OKGREEN': '\033[92m',
        'WARNING': '\033[93m',
        'FAIL': '\033[91m',
        'ENDC': '\033[0m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'}

    @staticmethod
    def input_error(): print(ConsoleMessages.colours['FAIL'] + "[FAIL]:Invalid input!" + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def no_game_data_found(): print(ConsoleMessages.colours['WARNING'] + "[WARN]:No data detected! Create or load existing data to proceed." + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def generic_success(): print(ConsoleMessages.colours['OKGREEN'] + "[OKAY]:Success!" + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def not_implemented(): print(ConsoleMessages.colours['INFOCYAN'] + "[INFO]:Not implemented!" + ConsoleMessages.colours['ENDC'] + '\n')

    @staticmethod
    def confirm_prompt(): print("Are you sure?\n"
                                + ConsoleMessages.colours['OKGREEN'] + "Y"
                                + ConsoleMessages.colours['ENDC'] + "/"
                                + ConsoleMessages.colours['FAIL'] + "N"
                                + ConsoleMessages.colours['ENDC'] + '\n')

    @staticmethod
    def ERRORMSG(message: str, haveKey: bool):
        if haveKey: print('\n' + ConsoleMessages.colours['FAIL'] + "[FAIL]:" + message + ConsoleMessages.colours['ENDC'] + '\n')
        else: print('\n' + ConsoleMessages.colours['FAIL'] + message + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def WARNMSG(message: str, haveKey: bool):
        if haveKey: print('\n' + ConsoleMessages.colours['WARNING'] + "[WARN]:" + message + ConsoleMessages.colours['ENDC'] + '\n')
        else: print('\n' + ConsoleMessages.colours['WARNING'] + message + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def OKMSG(message: str, haveKey: bool):
        if haveKey: print('\n' + ConsoleMessages.colours['OKGREEN'] + "[OKAY]:" + message + ConsoleMessages.colours['ENDC'] + '\n')
        else: print('\n' + ConsoleMessages.colours['OKGREEN'] + message + ConsoleMessages.colours['ENDC'] + '\n')
    @staticmethod
    def INFOMSG(message: str, haveKey: bool):
        if haveKey: print('\n' + ConsoleMessages.colours['INFOCYAN'] + "[INFO]:" + message + ConsoleMessages.colours['ENDC'] + '\n')
        else: print('\n' + ConsoleMessages.colours['INFOCYAN'] + message + ConsoleMessages.colours['ENDC'] + '\n')
