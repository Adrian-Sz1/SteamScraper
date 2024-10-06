from unittest import mock
from unittest.mock import mock_open

import pytest

from modules.helpers.file_manager import FileManager


class TestCheckForDuplicateNamesInDir:

    @staticmethod
    @pytest.fixture
    def mock_listdir(mocker):
        return mocker.patch('os.listdir')

    @staticmethod
    def test_no_duplicate_or_match(mock_listdir):
        mock_listdir.return_value = []
        result = FileManager.check_for_duplicate_names_in_dir("empty_directory", "testfile.json")
        assert result == "testfile.json"

    @staticmethod
    def test_single_file_in_dir_no_match(mock_listdir):
        mock_listdir.return_value = ["file_name.csv"]
        result = FileManager.check_for_duplicate_names_in_dir("single_file_directory", "file_name.json")
        assert result == "file_name.json"

    @staticmethod
    @pytest.mark.parametrize("files, file_name, expected", [
        (["file_name.json"], "file_name.json", "2_file_name.json"),
        (["testfile.txt", "image.png"], "testfile.txt", "2_testfile.txt"),
        (["duplicate_file.json", "duplicate_file.json"], "duplicate_file.json", "3_duplicate_file.json")
    ])
    def test_check_for_duplicate_names(mock_listdir, files, file_name, expected):
        mock_listdir.return_value = files
        result = FileManager.check_for_duplicate_names_in_dir("some_directory", file_name)
        assert result == expected

    @staticmethod
    def test_multiple_files_in_dir_same_extension_single_match(mock_listdir):
        mock_listdir.return_value = ["file_name.json", "some.json", "other.json", "names.json"]
        result = FileManager.check_for_duplicate_names_in_dir("multiple_file_directory", "file_name.json")
        assert result == "2_file_name.json"

    @staticmethod
    def test_multiple_files_in_dir_same_extension_three_matches(mock_listdir):
        mock_listdir.return_value = ["file_name.json", "file_name.json", "file_name.json", "names.json"]
        result = FileManager.check_for_duplicate_names_in_dir("multiple_file_directory", "file_name.json")
        assert result == "4_file_name.json"

    @staticmethod
    def test_multiple_files_in_dir_same_extension_three_partial_matches(mock_listdir):
        mock_listdir.return_value = ["2_file_name.json", "3_file_name.json", "4_file_name.json"]
        result = FileManager.check_for_duplicate_names_in_dir("multiple_file_directory", "file_name.json")
        assert result == "file_name.json"

    @staticmethod
    def test_same_name_different_extension(mock_listdir):
        mock_listdir.return_value = ["file_name.csv", "file_name.json"]
        result = FileManager.check_for_duplicate_names_in_dir("test_directory", "file_name.json")
        assert result == "2_file_name.json"

    @staticmethod
    @pytest.mark.parametrize("files, expected", [
        (["testfile.txt", "3_testfile.txt"], "2_testfile.txt"),
        (["9_testfile.txt", "6_testfile.txt", "testfile.txt"], "2_testfile.txt"),
    ])
    def test_increment_filename(mock_listdir, files, expected):
        mock_listdir.return_value = files
        result = FileManager.check_for_duplicate_names_in_dir("test_directory", "testfile.txt")
        assert result == expected

    @staticmethod
    def test_multiple_matches_file_not_ordered(mock_listdir):
        mock_listdir.return_value = ["9_testfile.txt",'6_testfile.txt',"testfile.txt", "3_testfile.txt"]
        result = FileManager.check_for_duplicate_names_in_dir("test_directory", "testfile.txt")
        assert result == "2_testfile.txt"

    @staticmethod
    def test_correct_return_value(mock_listdir):
        mock_listdir.return_value = ["duplicate_file.json"]
        result = FileManager.check_for_duplicate_names_in_dir("some_directory", "duplicate_file.json")
        assert result == "2_duplicate_file.json"

    @staticmethod
    def test_handles_nonexistent_directory():
        with pytest.raises(FileNotFoundError):
            FileManager.check_for_duplicate_names_in_dir("non_existent_dir", "new_file.json")

    @staticmethod
    def test_handles_special_characters(mock_listdir):
        mock_listdir.return_value = ["duplicate_file.json"]
        result = FileManager.check_for_duplicate_names_in_dir("some_directory", "duplicate_file@#$.json")
        assert result == "duplicate_file@#$.json"

    @staticmethod
    def test_case_sensitivity(mock_listdir):
        mock_listdir.return_value = ["File_Name.json", "file_name.json"]
        result = FileManager.check_for_duplicate_names_in_dir("test_directory", "file_name.json")
        assert result == "2_file_name.json"

class TestCheckDirectoryExists:

    @staticmethod
    @pytest.fixture
    def mock_exists(mocker):
        return mocker.patch('os.path.exists')

    @staticmethod
    @pytest.fixture
    def mock_makedirs(mocker):
        return mocker.patch('os.makedirs')

    @staticmethod
    def test_directory_exists(mock_exists):
        mock_exists.return_value = True
        result = FileManager.check_directory_exists("existing_dir")
        assert result is True

    @staticmethod
    def test_directory_does_not_exist_create_if_missing(mock_exists, mock_makedirs):
        mock_exists.return_value = False
        result = FileManager.check_directory_exists("non_existent_dir")
        mock_makedirs.assert_called_once_with("non_existent_dir")
        assert result is True

    @staticmethod
    def test_directory_does_not_exist_dont_create(mock_exists, mock_makedirs):
        mock_exists.return_value = False
        result = FileManager.check_directory_exists("non_existent_dir", create_if_missing=False)
        mock_makedirs.assert_not_called()
        assert result is False

    @staticmethod
    def test_directory_creation_failure(mock_exists, mock_makedirs):
        mock_exists.return_value = False
        mock_makedirs.side_effect = OSError("Failed to create directory")
        result = FileManager.check_directory_exists("non_existent_dir")
        mock_makedirs.assert_called_once_with("non_existent_dir")
        assert result is False

class TestConstructDefaultFileUserName:

    @staticmethod
    @pytest.fixture
    def mock_data(mocker):
        return mocker.patch('modules.currentDate', '05-10-2024')

    @staticmethod
    def test_construct_valid_file_user_name(mock_data):
        steam64id = '76561198000000000'
        file_type = 'json'
        expected_output = '76561198000000000_05-10-2024.json'

        result = FileManager.construct_default_file_user_name(steam64id, file_type)
        assert result == expected_output

    @staticmethod
    def test_construct_with_empty_steam64id(mock_data):
        steam64id = ''
        file_type = 'csv'
        with pytest.raises(TypeError):
            assert FileManager.construct_default_file_user_name(steam64id, file_type)

    @staticmethod
    def test_construct_with_empty_file_type(mock_data):
        steam64id = '76561198000000000'
        file_type = ''

        with pytest.raises(TypeError):
            assert FileManager.construct_default_file_user_name(steam64id, file_type)

@pytest.mark.usefixtures("mock_listdir", "mock_exists", "mock_join", "mock_open_function", "mock_valid_params", "mock_directory_check")
class TestCreateFileInDir:

    @staticmethod
    @pytest.fixture
    def mock_listdir(mocker):
        return mocker.patch('os.listdir', return_value=[])

    @staticmethod
    @pytest.fixture
    def mock_open_function(mocker):
        return mocker.patch('builtins.open', mock.mock_open())

    @staticmethod
    @pytest.fixture
    def mock_exists(mocker):
        return mocker.patch('os.path.exists', return_value=True)

    @staticmethod
    @pytest.fixture
    def mock_join(mocker):
        return mocker.patch('os.path.join', side_effect=lambda *args: '/'.join(args))

    @staticmethod
    @pytest.fixture
    def mock_valid_params(mocker):
        mocker.patch('modules.helpers.file_manager.FileManager.validate_parameters', return_value=True)

    @staticmethod
    @pytest.fixture
    def mock_directory_check(mocker):
        mocker.patch('modules.helpers.file_manager.FileManager.check_directory_exists')

    @staticmethod
    @pytest.fixture
    def mock_duplicate_name_check(mocker):
        return mocker.patch('modules.helpers.file_manager.FileManager.check_for_duplicate_names_in_dir', return_value='file(1).json')

    @staticmethod
    def test_create_file_valid(mock_open_function, mock_valid_params, mock_directory_check):
        working_dir = '/mock/path/to/'
        file_name = 'file.json'

        file = FileManager.create_file_in_dir(working_dir, file_name, overwrite=False)

        mock_open_function.assert_called_once_with('/mock/path/to/file.json', 'x')
        assert file is not None

    @staticmethod
    def test_create_file_existing(mock_open_function, mock_valid_params, mock_directory_check):
        working_dir = '/mock/path/to'
        file_name = 'file.json'

        mock_open_function.side_effect = [FileExistsError, mock_open()]

        file = FileManager.create_file_in_dir(working_dir, file_name, overwrite=True)

        mock_open_function.assert_called_with('/mock/path/to/file.json', 'w')
        assert file is not None

    @staticmethod
    def test_create_file_with_versioning(mock_open_function, mock_valid_params, mock_directory_check,
                                         mock_duplicate_name_check):
        working_dir = '/mock/path/to'
        file_name = 'file.json'

        file = FileManager.create_file_in_dir(working_dir, file_name, overwrite=False)

        mock_open_function.assert_called_once_with('/mock/path/to/file(1).json', 'x')
        assert file is not None

    @staticmethod
    @pytest.mark.parametrize("working_dir, file_name", [
        (5, 'file.json'),
        ('/valid/dir/', 123)
    ])
    def test_create_file_invalid_params(mock_open_function, mock_directory_check, working_dir, file_name):

        with pytest.raises(TypeError):
            assert FileManager.create_file_in_dir(working_dir, file_name) is None

    @staticmethod
    def test_create_file_directory_not_exist(mock_open_function, mock_valid_params, mock_directory_check):
        working_dir = '/mock/path/to'
        file_name = 'file.json'

        result = FileManager.create_file_in_dir(working_dir, file_name)

        assert result is not None

    @staticmethod
    def test_create_file_os_error(mock_open_function, mock_valid_params, mock_directory_check):
        working_dir = '/mock/path/to'
        file_name = 'file.json'

        mock_open_function.side_effect = OSError("Cannot create file")

        result = FileManager.create_file_in_dir(working_dir, file_name)

        assert result is None

@pytest.mark.usefixtures("mock_exists", "mock_join", "mock_valid_params", "mock_directory_check", "mock_open_function")
class TestFileManagerLoadFile:

    @staticmethod
    @pytest.fixture
    def mock_exists(mocker):
        return mocker.patch('os.path.exists', return_value=True)

    @staticmethod
    @pytest.fixture
    def mock_join(mocker):
        return mocker.patch('os.path.join', side_effect=lambda *args: '/'.join(args))

    @staticmethod
    @pytest.fixture
    def mock_valid_params(mocker):
        mocker.patch('modules.helpers.file_manager.FileManager.validate_parameters', return_value=True)

    @staticmethod
    @pytest.fixture
    def mock_directory_check(mocker):
        mocker.patch('modules.helpers.file_manager.FileManager.check_directory_exists', return_value=True)

    @staticmethod
    @pytest.fixture
    def mock_open_function(mocker):
        return mocker.patch('builtins.open', mock.mock_open(read_data="data"))

    @staticmethod
    def test_load_file_valid(mock_open_function):
        working_dir = '/mock/path/to'
        file_name = 'file.json'

        file = FileManager.load_file_in_dir(working_dir, file_name)

        mock_open_function.assert_called_once_with('/mock/path/to/file.json', 'r')

        assert file is not None

    @staticmethod
    def test_load_file_invalid_params():
        FileManager.validate_parameters = mock.Mock(return_value=False)

        working_dir = '/mock/path'
        file_name = 'file.json'

        file = FileManager.load_file_in_dir(working_dir, file_name)

        assert file is None

    @staticmethod
    def test_load_file_directory_does_not_exist():
        FileManager.check_directory_exists = mock.Mock(return_value=False)

        working_dir = '/mock/path'
        file_name = 'file.json'

        file = FileManager.load_file_in_dir(working_dir, file_name)

        assert file is None

    @staticmethod
    def test_load_file_os_error(mock_open_function):
        mock_open_function.side_effect = OSError("Mocked OS error")

        working_dir = '/mock/path'
        file_name = 'file.json'

        file = FileManager.load_file_in_dir(working_dir, file_name)

        assert file is None

class TestValidateParameters:

    @staticmethod
    @pytest.mark.parametrize("working_dir, file_name", [
        ('/valid/path', 'file.json'),
        ('C:\\valid\\path', 'file.csv'),
    ])
    def test_validate_parameters_valid(working_dir, file_name):
        result = FileManager.validate_parameters(working_dir, file_name)
        assert result is True

    @staticmethod
    @pytest.mark.parametrize("working_dir, file_name", [
        (None, 'file.json'),
        ('/valid/path', None),
        ('/valid/path', ''),
        ('/valid/path', ' '),
        (' ', 'file.json'),
        ('/valid/path', 'file'),
        (123, 'file.json'),
        ('/valid/path', 456),
    ])
    def test_validate_parameters_invalid(working_dir, file_name):
        result = FileManager.validate_parameters(working_dir, file_name)
        assert result is False

