from urllib.parse import urljoin
from flask import Flask


#GLOBALS
REPORTS_URL_PREFIX = '/reports'
SWITCHING_REPORTS_URL_PREFIX = '/switching_reports'
TELEPORT_SCHEDULE_URL_PREFIX = '/teleport'

REPORTS_URL_RULE_ENDPOINT = '/reports/static/'
SWITCHING_REPORTS_URL_RULE_ENDPOINT = '/switching_reports/static/'
TELEPORT_SCHEDULE_URL_RULE_ENDPOINT = '/teleport/static/'

PATH_FILE_NAME_CONST = '<path:filename>'

REPORTS_URL_RULE_STATIC_PATH = urljoin(REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
SWITCHING_REPORTS_URL_STATIC_PATH = urljoin(SWITCHING_REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
TELEPORT_SCHEDULE_URL_STATIC_PATH = urljoin(TELEPORT_SCHEDULE_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
#ENDGLOBALS

def registerServiceBlueprints(app:Flask, blueprints:list, url_prefix:str):
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

def addUrlRules(app):
    app.add_url_rule(REPORTS_URL_RULE_STATIC_PATH, endpoint=REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
    app.add_url_rule(SWITCHING_REPORTS_URL_STATIC_PATH, endpoint=SWITCHING_REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
    app.add_url_rule(TELEPORT_SCHEDULE_URL_STATIC_PATH, endpoint=TELEPORT_SCHEDULE_URL_RULE_ENDPOINT, view_func=app.send_static_file)
