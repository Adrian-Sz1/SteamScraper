import logging
from logging.handlers import MemoryHandler

from models.config_model import ConfigModel
from viewmodels.core_viewmodel import CoreViewModel

logger = logging.getLogger(__name__)


def main():
    temp_handler = MemoryHandler(capacity=10000, target=None)
    stream_handler = logging.StreamHandler()

    logging_format = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'
    formatter = logging.Formatter(logging_format, datefmt='%Y-%m-%d %H:%M:%S')

    temp_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[temp_handler, stream_handler])

    try:
        config = ConfigModel()
        config.load_config()

        file_handler = logging.FileHandler(config.root_directory + '/Steam_User_Scraper.log', delay=True)
        file_handler.setFormatter(formatter)

        logging.getLogger().addHandler(file_handler)
        temp_handler.setTarget(file_handler)
        temp_handler.flush()

        logging.getLogger().removeHandler(temp_handler)

    except Exception as e:
        logging.error("An error occurred while loading configuration", exc_info=True)

        temp_file_handler = logging.FileHandler('temp_log.log', delay=True)
        temp_file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(temp_file_handler)
        temp_handler.setTarget(temp_file_handler)
        temp_handler.flush()

        logging.getLogger().removeHandler(temp_handler)
        return

    viewmodel = CoreViewModel(config)
    viewmodel.run()


if __name__ == "__main__":

    logger.info('Starting Steam User Scraper')
    main()
    logger.info('Application shutting down...')
