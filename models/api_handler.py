import logging
import re

import requests

from modules.helpers.file_manager import InvalidParameterError

logger = logging.getLogger(__name__)

class SteamAPI:

    def __init__(self, api_key = ''):
        if not self.validate_steam_api_key_format(api_key):
            logger.warning(f"Api key '{api_key}' is not valid")
            # raise InvalidParameterError("Invalid API key format")
        self.api_key = api_key

    def __get__(self, instance, owner):
        return self.api_key

    def __set__(self, new_api_key: str):
        self.api_key = new_api_key
        logger.info(f"API key has been updated")

    def validate_api_key(self, api_key:str):

        r = SteamAPI.send_request_wrapper(self, 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + api_key + '&steamids=76561197960435530')
        if r.status_code == 200:
            logger.info('Steam API key is VALID')
        else:
            logger.info('Steam API key is INVALID')
        return r.status_code == 200


    def resolve_vanity_url(self, vanity_url_name: str):
        if not SteamAPI.validate_steam_api_key_format(self.api_key):
            logger.warning(f"Api key {self.api_key} is not valid")
            return None

        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={self.api_key}&vanityurl={vanity_url_name}"
        r = SteamAPI.send_request_wrapper(self, url)

        def on_success_callback():
            json_result = r.json()
            steam64id = json_result['response']['steamid']

            logger.info(f"Vanity url name {vanity_url_name} matches steam64id {steam64id}")
            return steam64id

        def on_bad_request_callback(): pass
        def on_unauthorized_callback(): pass
        def on_forbidden_callback(): pass
        def on_server_exception_callback(): pass

        return SteamAPI.response_handler(r.status_code,
                                on_success_callback,
                                on_bad_request_callback,
                                on_unauthorized_callback,
                                on_forbidden_callback,
                                on_server_exception_callback)

    def get_owned_games(self, steam64id: str):
        if not self.validate_steam_api_key_format(self.api_key):
            logger.warning(f"Api key {self.api_key} is not valid")
            return None

        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + self.api_key + '&steamid=' + steam64id + '&include_appinfo=false&include_played_free_games=true&format=json'
        r = self.send_request_wrapper(url)

        def on_success_callback():
            json_result = r.json()
            response_dict = json_result['response']
            if 'games' not in response_dict:
                logger.info(f"Games list for {steam64id} is empty - profile might be private")
                return None

            logger.info(f"Game list for {steam64id} has been retrieved. Game count [{response_dict['games'].__len__()}]")
            return response_dict

        def on_bad_request_callback(): pass
        def on_unauthorized_callback(): pass
        def on_forbidden_callback(): pass
        def on_server_exception_callback(): pass

        return SteamAPI.response_handler(r.status_code,
                                on_success_callback,
                                on_bad_request_callback,
                                on_unauthorized_callback,
                                on_forbidden_callback,
                                on_server_exception_callback)


    @staticmethod
    def validate_steam_api_key_format(api_key: str) -> bool:
        if not isinstance(api_key, str):
            raise InvalidParameterError(f"api_key should be of type str not of type {api_key.__class__()}")

        api_key_pattern = "^[A-Z0-9]{32}$"

        api_matches = re.match(api_key_pattern, api_key) is not None

        return api_matches


    def send_request_wrapper(self, url: str):
        r = requests.get(url)

        url = url.replace(self.api_key, '[STEAM API KEY REDACTED]')

        logger.info(''.join(['Status code ', str(r.status_code), ' for request ', url]))

        return r


    @staticmethod
    def response_handler(status_code: int,
                         on_success_callback,
                         on_bad_request_callback = None,
                         on_unauthorized_callback = None,
                         on_forbidden_callback = None,
                         on_server_exception_callback = None):
        match status_code:
            case 200:
                return on_success_callback()
            case 400:
                logger.warning(f"Encountered a bad request")
                if on_bad_request_callback:
                    return on_bad_request_callback()
            case 401:
                logger.warning(f"Could not retrieve game list due to unauthorized access")
                if on_unauthorized_callback:
                    return on_unauthorized_callback()
            case 403:
                logger.warning(f"Could not retrieve game list due to forbidden access")
                if on_forbidden_callback:
                    return on_forbidden_callback()
            case 500:
                logger.warning(f"Could not retrieve game list due to an unexpected server error")
                if on_server_exception_callback():
                    return on_server_exception_callback()
            case _:
                logger.warning(f"Encountered an unhandled status code {status_code}")
                return None