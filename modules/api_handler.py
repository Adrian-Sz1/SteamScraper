import modules.programsettings as ps
import logging
import os

import requests
import re
from modules.file_manager import InvalidParameterError

logger = logging.getLogger(__name__)

def validate_steam_api_key_format(api_key: str):
    if not isinstance(api_key, str):
        raise InvalidParameterError(f"api_key should be of type str not of type {api_key.__class__()}")

    api_key_pattern = '^[A-Z0-9]{32}$'

    return re.match(api_key_pattern, api_key)


def set_api_key(api_key:str):
    os.environ['Steam_API_Key'] = api_key
    logger.info('New Steam API Key set')


def get_api_key():
    return os.environ['Steam_API_Key']


def validate_api_key(api_key: str):

    r = sendRequestWrapper('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+api_key+'&steamids=76561197960435530')
    if r.status_code == 200:
        logger.info('Steam API key is VALID')
    else:
        logger.info('Steam API key is INVALID')
    return r.status_code == 200


def sendRequestWrapper(url: str):
    r = requests.get(url)

    if not ps.steam_api_key.isspace() and ps.steam_api_key.__len__() > 10:
         url = url.replace(ps.steam_api_key, '[STEAM API KEY REDACTED]')

    logger.info(''.join(['Status code ', str(r.status_code), ' for request ', url]))

    return r


def resolve_vanity_url(api_key: str, vanity_url_name: str):
    if not validate_steam_api_key_format(api_key):
        logger.warning(f"Api key {api_key} is not valid")
        return None

    url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={vanity_url_name}"
    r = sendRequestWrapper(url)

    match r.status_code:
        case 200:
            json_result = r.json()
            steam_id = json_result['response']['steamid']

            logger.info(f"Vanity url name {vanity_url_name} matches steam64id {steam_id}")
            return steam_id
        case 401:
            logger.info(f"Could not retrieve steam64id due to unauthorized access")
            return None
        case 403:
            logger.info(f"Could not retrieve steam64id due to forbidden access")
            return None
        case 500:
            logger.info(f"Could not retrieve steam64id due to an unexpected server error")
            return None
    return None


def get_owned_games(api_key: str, steam64_id: str):
    if not validate_steam_api_key_format(api_key):
        logger.warning(f"Api key {api_key} is not valid")
        return None

    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + api_key + '&steamid=' + steam64_id + '&include_appinfo=false&include_played_free_games=true&format=json'
    r = sendRequestWrapper(url)

    match r.status_code:
        case 200:
            json_result = r.json()
            response_dict = json_result['response']
            if 'games' not in response_dict:
                logger.info(f"Games list for {steam64_id} is empty, profile might be private")
                return None

            logger.info(f"Game list for {steam64_id} has been retrieved. Game count [{response_dict['games'].__len__()}]")
            return response_dict
        case 401:
            logger.warning(f"Could not retrieve game list due to unauthorized access")
            return None
        case 403:
            logger.warning(f"Could not retrieve game list due to forbidden access")
            return None
        case 500:
            logger.warning(f"Could not retrieve game list due to an unexpected server error")
            return None
    return None