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
