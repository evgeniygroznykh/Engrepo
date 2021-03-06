import json
from models.logger import handleGeneralExceptions


def getConfigFromJson():
    try:
        with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
            config_json = json.load(read_json_config)
        return config_json
    except FileNotFoundError as exc:
        handleGeneralExceptions(exc, "Log file wasn't found.")


external_config = getConfigFromJson()
