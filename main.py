import modules.gui
from modules.programsettings import readSettings
import modules.programsettings as ps
import logging

logger = logging.getLogger(__name__)


def initialize():
    logger.info('Starting Initialization')
    readSettings()

    modules.gui.create_window(ps.output_folder_path, ps.output_file_type, ps.create_sub_folders, ps.previous_parameters,
                              ps.steam_api_key, ps.search_options)


if __name__ == "__main__":
    FORMAT = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'

    logging.basicConfig(
                        level=logging.INFO,
                        format=FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(ps.getAppDataPath() + '/Steam_User_Scraper.log'),
                                  logging.StreamHandler()])

    logger.info('Starting Steam User Scraper')
    initialize()
    logger.info('Process finished with exit code 0')
