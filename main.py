import modules.gui
from modules.programsettings import readSettings
import modules.programsettings as ps


def initialize():
    readSettings()
    modules.gui.create_window(ps.output_folder_path, ps.output_file_type, ps.create_sub_folders, ps.previous_parameters, ps.steam_api_key)


if __name__ == "__main__":
    initialize()
