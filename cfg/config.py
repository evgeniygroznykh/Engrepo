import json


def get_tags():
    with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
        tags_json = json.load(read_json_config)
    return tags_json['tags']