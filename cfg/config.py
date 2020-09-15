import json


def get_tags():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['tags']

def get_users():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['users']

def get_work_types():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['work types']

def get_customers():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['customers']

def get_shifts():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['shifts']

def get_sources():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['sources']

def get_destinations():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        config_json = json.load(read_json_config)
    return config_json['destinations']