import modules
import modules.enums.file_types as file_types
import os.path
import logging

logger = logging.getLogger(__name__)


def construct_default_file_user_name(steam_id: str, file_type: str):
    return steam_id + '_' + modules.currentDate + '.' + file_type


def construct_custom_file_name(name: str, file_type: str):
    if not validate_file_type(file_type): return False

    return name + '.' + file_type


def construct_file_dir_default_path(folder_path: str, file_type: str):
    return folder_path + '/' + file_type + '/'


def construct_file_dir_user_sub_folders(folder_path: str, file_type: str, steam_id: str):
    return folder_path + '/' + file_type + '/' + steam_id + '/'


def validate_file_type(file_type: str):
    """
    Checks if the file type provided is supported by the program. For full list, see ../modules/enums.file_types.py
    """
    if not file_types.SupportedFileType.is_supported(file_type):
        logger.warning(f"{file_type} is not supported")
        return False
    return True


def create_file_in_dir(folder_path: str, file_name: str):
    """
    Attempts to create a new file in the directory specified with a given file name.
    :param str folder_path: absolute path to the folder directory where the file should be saved
    :param str file_name: name of the file to be saved, must include a file type but the specific type is not enforced
    :returns: true if successful, false if failed or if file already exists
    """
    try:
        if not isinstance(folder_path, str):
            raise TypeError(f"{folder_path} is not of type string")
        if not isinstance(file_name, str):
            raise TypeError(f"{file_name} is not of type string")

        if file_name is None or file_name.isspace():
            raise InvalidParameterError('file_name is null, empty or whitespace')
        if folder_path is None or folder_path.isspace():
            raise InvalidParameterError("folder_path is null, empty, or whitespace")

        if not os.path.splitext(file_name)[1]:
            raise InvalidParameterError(f"File name '{file_name}' does not contain a file extension")

    except (TypeError, InvalidParameterError) as e:
        logger.exception(f"Parameter validation failed: {e}")
        return None

    folder_path = os.path.join(folder_path, '')  # Ensures that a trailing forward slash (/) is present at the end of the string
    full_path = os.path.join(folder_path, file_name)

    if os.path.exists(full_path):
        logger.info(f"File at '{full_path}' already exists")
        return open(full_path, 'w') # TODO: Add a check here if we want to overwrite the files or make new ones

    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            logger.info(f"Directory '{folder_path}' created")
        except OSError as e:
            logger.exception(f"Failed to create directory '{folder_path}': {e}")
            return None

    try:
        file = open(full_path, 'x')
        logger.info(f"File '{full_path}' has been created")
        return file
    except FileExistsError:
        logger.info(f"File '{full_path}' already exists after directory creation")
        return None
    except OSError as e:
        logger.exception(f"Error creating file '{full_path}': {e}")
        return None


class InvalidParameterError(Exception):
    """Raised when a parameter of type string is None, empty or whitespace"""

    def __init__(self, message="Invalid parameter: None, empty, or whitespace string."):
        super().__init__(message)
