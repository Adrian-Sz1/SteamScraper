import json
from textwrap import indent

import pytest
from unittest.mock import mock_open, patch

import yaml

from modules.helpers.file_exporters import FileExporters


@pytest.fixture
def mock_file():
    with patch('builtins.open', mock_open()) as mocked_file:
        yield mocked_file


class TestGenerateCsvDataFile:

    @staticmethod
    def test_generate_csv_valid_data(mock_file):
        content = {
            'game_data': {
                'games': [
                    {'name': 'Game 1', 'hours_played': 10},
                    {'name': 'Game 2', 'hours_played': 20}
                ]
            }
        }


        file_mock = mock_file.return_value
        FileExporters.generate_csv_data_file(file_mock, content)

        written_data = ''.join(call.args[0] for call in file_mock.write.call_args_list)

        normalized_written_data = written_data.replace('\r\n', '\n') # CRLF -> LF line endings

        expected_csv_output = "name,hours_played\nGame 1,10\nGame 2,20\n"
        assert normalized_written_data == expected_csv_output

    @staticmethod
    def test_generate_csv_empty_game_list(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': []
            }
        }
        with pytest.raises(ValueError):
            FileExporters.generate_csv_data_file(file_mock, content)

    @staticmethod
    def test_generate_csv_invalid_file():
        file = None
        content = {
            'game_data': {
                'games': [{'name': 'Game 1', 'hours_played': 10}]
            }
        }

        with pytest.raises(FileNotFoundError):
            FileExporters.generate_csv_data_file(file, content)

    @staticmethod
    def test_generate_csv_data_file_missing_games_key(mock_file):
        file_mock = mock_file.return_value
        content = {'game_data': {}}

        with pytest.raises(ValueError):
            FileExporters.generate_csv_data_file(file_mock, content)

    @staticmethod
    def test_generate_csv_data_file_malformed_game_entries(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': ['invalid_entry']
            }
        }

        with pytest.raises(ValueError):
            FileExporters.generate_csv_data_file(file_mock, content)

class TestGenerateJsonDataFile:

    @staticmethod
    def test_generate_json_valid_data(mock_file):
        content = {
            'game_data': {
                'games': [
                    {'name': 'Game 1', 'hours_played': 10},
                    {'name': 'Game 2', 'hours_played': 20}
                ]
            }
        }

        file_mock = mock_file.return_value
        FileExporters.generate_json_data_file(file_mock, content)

        expected_csv_output = json.dumps(content, indent=2)

        file_mock.write.assert_called_once_with(expected_csv_output)

        file_mock.close.assert_called_once()


    @staticmethod
    def test_generate_json_empty_game_list(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': []
            }
        }
        with pytest.raises(ValueError):
            FileExporters.generate_json_data_file(file_mock, content)

    @staticmethod
    def test_generate_json_invalid_file():
        file = None
        content = {
            'game_data': {
                'games': [{'name': 'Game 1', 'hours_played': 10}]
            }
        }

        with pytest.raises(FileNotFoundError):
            FileExporters.generate_json_data_file(file, content)

    @staticmethod
    def test_generate_json_data_file_missing_games_key(mock_file):
        file_mock = mock_file.return_value
        content = {'game_data': {}}

        with pytest.raises(ValueError):
            FileExporters.generate_json_data_file(file_mock, content)

    @staticmethod
    def test_generate_json_data_file_malformed_game_entries(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': ['invalid_entry']
            }
        }

        file_mock = mock_file.return_value
        FileExporters.generate_json_data_file(file_mock, content)

        expected_csv_output = json.dumps(content, indent=2)

        file_mock.write.assert_called_once_with(expected_csv_output)

        file_mock.close.assert_called_once()

class TestGenerateYamlDataFile:

    @staticmethod
    def test_generate_yaml_valid_data(mock_file):
        content = {
            'game_data': {
                'games': [
                    {'name': 'Game 1', 'hours_played': 10},
                    {'name': 'Game 2', 'hours_played': 20}
                ]
            }
        }

        file_mock = mock_file.return_value
        FileExporters.generate_yaml_data_file(file_mock, content)

        expected_yaml_output = yaml.dump(content, allow_unicode=True)
        written_content = "".join(call.args[0] for call in file_mock.write.call_args_list)

        assert written_content == expected_yaml_output

        file_mock.close.assert_called_once()

    @staticmethod
    def test_generate_yaml_empty_game_list(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': []
            }
        }
        with pytest.raises(ValueError):
            FileExporters.generate_yaml_data_file(file_mock, content)

    @staticmethod
    def test_generate_yaml_invalid_file():
        file = None
        content = {
            'game_data': {
                'games': [{'name': 'Game 1', 'hours_played': 10}]
            }
        }

        with pytest.raises(FileNotFoundError):
            FileExporters.generate_yaml_data_file(file, content)

    @staticmethod
    def test_generate_yaml_data_file_missing_games_key(mock_file):
        file_mock = mock_file.return_value
        content = {'game_data': {}}

        with pytest.raises(ValueError):
            FileExporters.generate_yaml_data_file(file_mock, content)

    @staticmethod
    def test_generate_yaml_data_file_malformed_game_entries(mock_file):
        file_mock = mock_file.return_value
        content = {
            'game_data': {
                'games': ['invalid_entry']
            }
        }

        FileExporters.generate_yaml_data_file(file_mock, content)

        expected_yaml_output = yaml.dump(content, allow_unicode=True)
        written_content = "".join(call.args[0] for call in file_mock.write.call_args_list)

        assert written_content == expected_yaml_output

        file_mock.close.assert_called_once()