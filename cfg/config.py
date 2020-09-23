import json
import os
from models.logger import createLogFilesDirIfNotExists, logFileNotFoundErrorAndReraise



def getConfigAsJson():
    try:
    	createLogFilesDirIfNotExists()

        with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
            config_json = json.load(read_json_config)
        return config_json
    except FileNotFoundError as exc:
        logFileNotFoundErrorAndReraise()

def getGlobalConfigSettingsNames(json_config):
	return [setting_name for setting_name in json_config.keys()]

def getGlobalConfigValues(json_config):
	return [config_value for config_value in json_config.values()]

def representConfigValuesAsDict(config_settings_names, config_values):
	return { k:v for k in config_settings_names for v in global_config_values } 


