import pytest

from modules.helpers.common import validate_steam64id_format, remap_output_game_data


class TestValidateSteam64IdFormat:

    @staticmethod
    def test_valid_steam64id():
        valid_steam_id = '76561198034329453'
        assert validate_steam64id_format(valid_steam_id) is True

    @staticmethod
    def test_steam64id_not_numeric():
        invalid_steam_id = '76561198034ABCDE'
        assert validate_steam64id_format(invalid_steam_id) is False

    @staticmethod
    def test_steam64id_short_length():
        invalid_steam_id_short = '7656119803432945'  # 16 characters
        assert validate_steam64id_format(invalid_steam_id_short) is False

    @staticmethod
    def test_steam64id_long_length():
        invalid_steam_id_long = '765611980343294533'  # 18 characters
        assert validate_steam64id_format(invalid_steam_id_long) is False

    @staticmethod
    def test_steam64id_invalid_type():
        invalid_steam_id = 76561198034329453
        with pytest.raises(TypeError):
            validate_steam64id_format(invalid_steam_id)

    @staticmethod
    def test_steam64id_empty_string():
        invalid_steam_id = ''
        assert validate_steam64id_format(invalid_steam_id) is False

    @staticmethod
    def test_steam64id_with_spaces():
        invalid_steam_id = '76561198034329 53'
        assert validate_steam64id_format(invalid_steam_id) is False


class TestRemapOutputGameData:

    @staticmethod
    def test_remap_with_valid_data():
        game_data = {
            'game_count': 2,
            'games': [
                {'playtime_forever': 50, 'playtime_2weeks': 10},
                {'playtime_forever': 100, 'playtime_2weeks': 20}
            ]
        }
        expected_output = {
            'game_data': {
                'game_count': 2,
                'total_playtime': 150,
                'total_playtime_last_2weeks': 30,
                'games': game_data['games']
            }
        }
        assert remap_output_game_data(game_data) == expected_output

    @staticmethod
    def test_remap_with_missing_game_count():
        game_data = {
            'games': [
                {'playtime_forever': 40, 'playtime_2weeks': 15},
                {'playtime_forever': 70, 'playtime_2weeks': 15}
            ]
        }
        expected_output = {
            'game_data': {
                'game_count': 2,
                'total_playtime': 110,
                'total_playtime_last_2weeks': 30,
                'games': game_data['games']
            }
        }
        assert remap_output_game_data(game_data) == expected_output

    @staticmethod
    def test_remap_with_empty_games_list():
        game_data = {
            'game_count': 0,
            'games': []
        }
        expected_output = {
            'game_data': {
                'game_count': 0,
                'total_playtime': 0,
                'total_playtime_last_2weeks': 0,
                'games': []
            }
        }
        assert remap_output_game_data(game_data) == expected_output

    @staticmethod
    def test_remap_with_partial_game_data():
        game_data = {
            'games': [
                {'playtime_forever': 25},
                {'playtime_forever': 60, 'playtime_2weeks': 0}
            ]
        }
        expected_output = {
            'game_data': {
                'game_count': 2,
                'total_playtime': 85,
                'total_playtime_last_2weeks': 0,
                'games': game_data['games']
            }
        }
        assert remap_output_game_data(game_data) == expected_output

    @staticmethod
    def test_remap_with_empty_input():
        game_data = {}
        expected_output = {
            'game_data': {
                'game_count': 0,
                'total_playtime': 0,
                'total_playtime_last_2weeks': 0,
                'games': []
            }
        }
        assert remap_output_game_data(game_data) == expected_output
