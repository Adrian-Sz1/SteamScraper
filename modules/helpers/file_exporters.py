import json
import csv
import yaml
import logging

logger = logging.getLogger(__name__)

class FileExporters:

    @staticmethod
    def generate_json_data_file(file, content: dict):
        """
            Generates a JSON data file from the provided content.
            The file is closed after writing the content.

            :param file: The file object to which the JSON content will be written.
            :param content: The content to be converted into JSON format and written to the file.
        """

        games = content.get('game_data', {}).get('games', [])

        if not file:
            raise FileNotFoundError("File provided could not be accessed or doesn't exist")

        if not games:
            raise ValueError("No game data available to generate Json file.")

        save_file_json = json.dumps(content, indent=2)

        file.write(save_file_json)

        file.close()

        logger.info('Json data file created for "' + file.name + '"')

    @staticmethod
    def generate_yaml_data_file(file, content: dict):
        """
        Generates a YAML data file with the given content.
        The file is closed after writing the content.

        :param file: The file object to which the YAML content will be written.
        :param content: The content to be converted into YAML format and written to the file.
        """
        games = content.get('game_data', {}).get('games', [])

        if not file:
            raise FileNotFoundError("File provided could not be accessed or doesn't exist")

        if not games:
            raise ValueError("No game data available to generate Json file.")

        yaml.dump(content, file, allow_unicode=True)

        file.close()

        logger.info('Yaml data file created for "' + file.name + '"')

    @staticmethod
    def generate_csv_data_file(file, content: dict):
        """
        Generates a CSV data file from the given content dictionary.

        Given a dictionary with a 'games' key, which contains a list of dictionaries
        representing game data, this function writes that data into the specified file
        in CSV format.

        Args:
            file: An open file object where the CSV data will be written.
            content (dict): A dictionary containing a 'games' key with the game data.

        Raises:
            KeyError: If the 'games' key is not found in the content dictionary.
            IOError: If there are any issues with file operations.

        The 'games' key in the content dictionary should map to a list of dictionaries.
        Each dictionary in the list represents a row, and the keys of the dictionaries
        represent the column headers for the CSV file.
        """

        games = content.get('game_data', {}).get('games', [])

        if not file:
            raise FileNotFoundError("File provided could not be accessed or doesn't exist")

        if not games:
            raise ValueError("No game data available to generate CSV file.")

        first_game = games[0]
        if not isinstance(first_game, dict):
            raise ValueError("Game element should be a dictionary.")

        headers = first_game.keys()

        with file as f:
            w = csv.DictWriter(f, headers)
            w.writeheader()
            for game in games:
                w.writerow(game)

        f.close()

        logger.info('Csv data file created for "' + file.name)