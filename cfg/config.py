import json


def get_json_config():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json
