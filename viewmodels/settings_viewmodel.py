from PySide6.QtCore import QObject, Signal

from models.settings_model import SettingsModel


class SettingsViewModel(QObject):
    outputFolderPathChanged = Signal(str)
    outputFileTypeChanged = Signal(str)
    createSubFoldersChanged = Signal(bool)
    overwriteEnabledChanged = Signal(bool)
    previousParametersChanged = Signal(str)
    steamApiKeyChanged = Signal(str)
    searchOptionsChanged = Signal(object)

    def __init__(self, working_dir: str = ''):
        super().__init__()
        self._preferences = SettingsModel(working_dir)
        self._preferences.load_settings()
        
    @property
    def output_folder_path(self):
        return self._preferences.output_folder_path

    @output_folder_path.setter
    def output_folder_path(self, value):
        self._preferences.output_folder_path = value
        self.outputFolderPathChanged.emit(value)

    @property
    def output_file_type(self):
        return self._preferences.output_file_type

    @output_file_type.setter
    def output_file_type(self, value):
        self._preferences.output_file_type = value
        self.outputFileTypeChanged.emit(value)

    @property
    def create_sub_folders(self):
        return self._preferences.create_sub_folders

    @create_sub_folders.setter
    def create_sub_folders(self, value):
        self._preferences.create_sub_folders = value
        self.createSubFoldersChanged.emit(value)

    @property
    def overwrite_enabled(self):
        return self._preferences.overwrite_enabled

    @overwrite_enabled.setter
    def overwrite_enabled(self, value):
        self._preferences.overwrite_enabled = value
        self.overwriteEnabledChanged.emit(value)

    @property
    def previous_parameters(self):
        return self._preferences.previous_parameters

    @previous_parameters.setter
    def previous_parameters(self, value):
        self._preferences.previous_parameters = value
        self.previousParametersChanged.emit(value)

    @property
    def steam_api_key(self):
        return self._preferences.steam_api_key

    @steam_api_key.setter
    def steam_api_key(self, value):
        self._preferences.steam_api_key = value
        self.steamApiKeyChanged.emit(value)

    @property
    def search_options(self):
        return self._preferences.search_options

    @search_options.setter
    def search_options(self, value):
        self._preferences.search_options = value
        self.searchOptionsChanged.emit(value)
        
        
        