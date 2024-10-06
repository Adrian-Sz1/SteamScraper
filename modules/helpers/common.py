import logging
from enum import Enum
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OutputUserStatus(Enum):
    NOT_FOUND = 'User not found'
    ACCOUNT_PRIVATE = 'Account is private'
    UNEXPECTED_ERROR = 'Unexpected error has occurred'
    SUCCESSFUL = 'Success'


def validate_steam64id_format(steam64_id: str):
    """
    Validates the provided steam64id is numeric and of length 17

    Args:
        steam64_id (str): The id to be validated

    Returns:
        True if provided steam64id meets the criteria, false otherwise

    Raises:
        TypeError: On invalid type of steam64id provided
    """
    if not isinstance(steam64_id, str):
        raise TypeError(f"steam_id: {steam64_id} is not of a valid type '{steam64_id.__class__}'. Should be of type 'str''")

    if not steam64_id.isnumeric() or steam64_id.__len__() != 17:
        logger.warning(f"Steam64Id: {steam64_id} is invalid. Not numeric or length is not 17 chars long")
        return False

    return True


def remap_output_game_data(game_data: Dict[str, Any]):
    """
    Remaps the output game data by calculating total playtime and total playtime for the last 2 weeks.

    Args:
        game_data: Dictionary containing game data with keys 'games' and 'game_count'.

    Returns:
         A remapped dictionary with game data including total playtime and playtime for the last 2 weeks.
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
