import json
from models.logger import logFileNotFoundErrorAndReraise


class Config:
    @staticmethod
    def getConfigFromJson():
        try:
            with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
                config_json = json.load(read_json_config)
            return config_json
        except FileNotFoundError:
            logFileNotFoundErrorAndReraise()

external_config = Config.getConfigFromJson()
