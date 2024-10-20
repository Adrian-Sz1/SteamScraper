import logging

from PySide6.QtCore import QObject, Signal, Slot

from models.api_handler import SteamAPI

logger = logging.getLogger(__name__)


class ApiHandlerViewModel(QObject):
    apiKeyChanged = Signal(str)
    apiValidationStatusChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._steam_api = SteamAPI()
        self._api_key = ''

    @property
    def api_key(self):
        return self._steam_api.api_key

    @Slot(str)
    def test(self, key: str):
        if self._api_key != key:
            self._api_key = key
            self._steam_api.api_key = key
            self.apiKeyChanged.emit(key)

    @api_key.setter
    def api_key(self, key: str):
        if self._api_key != key:
            self._api_key = key
            self._steam_api.api_key = key
            self.apiKeyChanged.emit(key)

    @Slot()
    def validate_api_key(self):
        is_valid = self._steam_api.validate_api_key(self.api_key)
        self.apiValidationStatusChanged.emit(is_valid)
        return is_valid

    def resolve_vanity_url(self, vanity_url_name: str):
        return self._steam_api.resolve_vanity_url(vanity_url_name)

    def get_owned_games(self, steam64id: str):
        return self._steam_api.get_owned_games(steam64id)
