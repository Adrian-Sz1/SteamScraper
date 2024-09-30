import json
import csv
import yaml
import logging

logger = logging.getLogger(__name__)


def generateJsonDataFile(file, content):

    save_file_json = json.dumps(content, indent=2)

    file.write(save_file_json)

    file.close()

    logger.info('Json data file created for "' + file.name + '"')


def generateYamlDataFile(file, content):
    yaml.dump(content, file, allow_unicode=True)

    file.close()

    logger.info('Yaml data file created for "' + file.name + '"')


def generateCsvDataFile(file, content: dict):
    games = content['games']
    games1 = games[0].keys()
    with file as f:
        w = csv.DictWriter(f, games1)
        w.writeheader()
        for game in games:
            w.writerow(game)

    f.close()

    logger.info('Csv data file created for "' + file.name)

    return True
