import logging

from PySide6.QtCore import QObject

from models.config_model import ConfigModel

logger = logging.getLogger(__name__)


class ConfigViewModel(QObject):
    def __init__(self):
        super(ConfigViewModel, self).__init__()
        self._model = ConfigModel()
        self._model.load_config()

    @property
    def app_name(self):
        return self._model.app_name

    @property
    def root_directory(self):
        return self._model.root_directory

    @property
    def build_version(self):
        return self._model.build_version

    @property
    def copyright_license(self):
        return self._model.copyright_license

    @property
    def author(self):
        return self._model.author

    @property
    def font(self):
        return self._model.font