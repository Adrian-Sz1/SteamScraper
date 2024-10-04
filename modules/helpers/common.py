from enum import Enum
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OutputUserStatus(Enum):
    NOT_FOUND = 'User not found'
    ACCOUNT_PRIVATE = 'Account is private'
    UNEXPECTED_ERROR = 'Unexpected error has occurred'
    SUCCESSFUL = 'Success'


def parseDictToString(unparsedOutput: dict):
    output = ''

    for key in unparsedOutput:
        output += '[' + key + '] ' + unparsedOutput[key] + '\n'

    return output


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


def listToString(content: list, delimiter: str):
    output = ''
    for element in content:
        output += element + delimiter

    output = output.removesuffix(delimiter)

    return output


def dictToString(content: dict, delimiter: str):
    """
    Only works for one-dimensional dictionaries
    """

    output = ''
    for key in content:
        output += key + '=' + str(content[key]) + delimiter

    output = output.removesuffix(delimiter)

    return output


def validate_steam64id_format(steam_id: str):
    if not isinstance(steam_id, str):
        raise TypeError(f"steam_id: {steam_id} is not of a valid type '{steam_id.__class__}'. Should be of type 'str''")

    if not steam_id.isnumeric() or steam_id.__len__() != 17:
        logger.warning(f"Steam64Id: {steam_id} is invalid. Not numeric or length is not 17 chars long")
        return False

    return True


def remap_output_game_data(game_data: Dict[str, Any]):
    """
    Remaps the output game data by calculating total playtime and total playtime for the last 2 weeks.

    :param game_data: Dictionary containing game data with keys 'games' and 'game_count'.
    :return: A remapped dictionary with game data including total playtime and playtime for the last 2 weeks.
    """
    games_dict = game_data.get('games', [])

    total_playtime = 0
    total_playtime_last_2weeks = 0

    for game in games_dict:
        total_playtime += game.get('playtime_forever', 0)
        total_playtime_last_2weeks += game.setdefault('playtime_2weeks', 0)

    output_template = {
        "game_data": {
            "game_count": game_data.get('game_count', len(games_dict)),
            "total_playtime": total_playtime,
            "total_playtime_last_2weeks": total_playtime_last_2weeks,
            "games": games_dict
        }
    }

    return output_template
