import json


def get_json_config():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json

#GLOBALS
JSON_CONFIG = get_json_config()
TAGS, USERS, CUSTOMERS, WORK_TYPES,\
SHIFTS, SOURCES, DESTINATIONS, \
UPLOAD_FOLDER, MAX_FILE_SIZE = [config_value for config_value in JSON_CONFIG.values()]




