import modules.enums.file_types as file_types
import modules
import os.path
import logging

logger = logging.getLogger(__name__)

class FileManager:

    @staticmethod
    def check_directory_exists(dir_path: str, create_if_missing: bool = True) -> bool:
        """
        Verifies the existence of a specified directory and creates it if it doesn't exist.
        Parameter create_if_missing should be set to False for file paths that include names of files.
        This method only creates directories not individual files.

        Args:
            dir_path (str): The path of the directory to check.
            create_if_missing (bool): If True, creates the directory if it does not exist. Defaults to True.

        Returns:
            bool: True if the directory exists or was successfully created, False otherwise.
        """
        if not os.path.exists(dir_path):
            if not create_if_missing:
                logger.info(f"Directory '{dir_path}' could not be found.")
                return False
            try:
                os.makedirs(dir_path)
                logger.info(f"Created missing directory: '{dir_path}'")
            except OSError as e:
                logger.exception(f"Failed to create directory '{dir_path}': {e}")
                return False
        logger.info(f"Directory '{dir_path}' found.")
        return True

    @staticmethod
    def construct_default_file_user_name(steam64id: str, file_type: str):
        return steam64id + '_' + modules.currentDate + '.' + file_type

    @staticmethod
    def construct_custom_file_name(name: str, file_type: str):
        return name + '.' + file_type

    @staticmethod
    def construct_file_dir_default_path(folder_path: str, file_type: str):
        return folder_path + '/' + file_type + '/'

    @staticmethod
    def construct_file_dir_user_sub_folders(folder_path: str, file_type: str, steam64id: str):
        return folder_path + '/' + file_type + '/' + steam64id + '/'

    @staticmethod
    def validate_file_type(file_type: str):
        """
        Checks if the file type provided is supported by the program. For full list, see ../modules/enums.file_types.py
        """
        if not file_types.SupportedFileType.is_supported(file_type):
            logger.warning(f"{file_type} is not supported")
            return False
        return True

    @staticmethod
    def validate_parameters(working_dir, file_name: str):
        try:
            if not isinstance(working_dir, str):
                raise TypeError(f"{working_dir} is not of type string")
            if not isinstance(file_name, str):
                raise TypeError(f"{file_name} is not of type string")

            if file_name is None or file_name.isspace():
                raise InvalidParameterError('file_name is null, empty or whitespace')
            if working_dir is None or working_dir.isspace():
                raise InvalidParameterError("folder_path is null, empty, or whitespace")

            if not os.path.splitext(file_name)[1]:
                raise InvalidParameterError(f"File name '{file_name}' does not contain a file extension")

        except (TypeError, InvalidParameterError) as e:
            logger.exception(f"Parameter validation failed: {e}")
            return False

        return True

    @staticmethod
    def create_file_in_dir(working_dir: str, file_name: str, overwrite: bool = False):
        """
        Attempts to create a new file in the directory specified with a given file name.
        :param str file_name: name of the file to be saved, must include a file type but the specific type is not enforced
        :param bool overwrite: if true, the file with the same name will be overwritten, else file versioning will be applied e.g. file1.json, file1(1).json
        :returns: file object if file created or already exists, None if failed
        """
        if not FileManager.validate_parameters(working_dir, file_name): return None

        FileManager.check_directory_exists(working_dir, True)

        if not overwrite:
            file_name = FileManager.check_for_duplicate_names_in_dir(working_dir, file_name)

        full_path = os.path.join(working_dir, file_name)

        mode = 'w' if overwrite else 'x'
        try:
            file = open(full_path, mode)
            logger.info(f"File '{full_path}' has been created or opened in '{mode}' mode.")
            return file
        except FileExistsError:
            logger.info(f"File '{full_path}' exists, opening in 'w' mode instead.")
            return open(full_path, 'w')
        except OSError as e:
            logger.exception(f"Error creating file '{full_path}': {e}")
            return None

    @staticmethod
    def load_file_in_dir(working_dir: str, file_name: str):
        """
        Loads a file located in the working directory if it exists.

        This method attempts to open the specified file in read mode from the working directory.
        If the file does not exist, an informational log is recorded and None is returned.
        If an error occurs while trying to open the file, an exception log is recorded.

        Parameters:
            file_name (str): The name of the file to be loaded.

        Returns:
            TextIO or None: The file object if successfully loaded; otherwise, None.
        """
        if not FileManager.validate_parameters(working_dir, file_name): return None

        full_path = os.path.join(working_dir, file_name)

        if not FileManager.check_directory_exists(full_path, False):
            return None

        try:
            file = open(full_path, 'r')
            logger.info(f"File '{full_path}' has been loaded")
            return file
        except OSError as e:
            logger.exception(f"Error loading file '{full_path}': {e}")

        return None

    @staticmethod
    def check_for_duplicate_names_in_dir(target_dir: str, file_name: str):
        files_in_dir = os.listdir(target_dir)

        counter = 0

        for file in files_in_dir:
            if not file.__contains__(file_name):
                continue
            counter += 1

        if counter == 0:
            return file_name

        return f"{counter+1}_{file_name}"



class InvalidParameterError(Exception):
    """Raised when a parameter of type string is None, empty or whitespace"""

    def __init__(self, message="Invalid parameter: None, empty, or whitespace string."):
        super().__init__(message)
