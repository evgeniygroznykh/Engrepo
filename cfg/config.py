import json
from datetime import datetime as dt


def get_json_config():
    try:
        with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
            config_json = json.load(read_json_config)
        return config_json
    except FileNotFoundError as exc:
        with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
            print(f"{dt.now()} | Config file was not found. | {exc.strerror} => {exc.filename}", file=log_file)
        raise

#GLOBALS
JSON_CONFIG = get_json_config()
TAGS, USERS, CUSTOMERS, WORK_TYPES,\
SHIFTS, SOURCES, DESTINATIONS, \
UPLOAD_FOLDER, MAX_FILE_SIZE = [config_value for config_value in JSON_CONFIG.values()]




