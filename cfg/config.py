import json
import os
from models.logger import log_file_not_found_and_reraise


def get_json_config():
    try:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
            config_json = json.load(read_json_config)
        return config_json
    except FileNotFoundError as exc:
        log_file_not_found_and_reraise(exc, 'Config file was not found.')

#GLOBALS
JSON_CONFIG = get_json_config()
TAGS, USERS, CUSTOMERS, WORK_TYPES,\
SHIFTS, SOURCES, DESTINATIONS, \
UPLOAD_FOLDER, MAX_FILE_SIZE, DATABASE_URI = [config_value for config_value in JSON_CONFIG.values()]
