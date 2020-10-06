from urllib.parse import urljoin
from flask import Flask


#GLOBALS
REPORTS_URL_RULE_ENDPOINT = '/reports/static/'
SWITCHING_REPORTS_URL_RULE_ENDPOINT = '/switching_reports/static/'
CONFIGURATOR_URL_RULE_ENDPOINT = '/configurator/static/'

PATH_FILE_NAME_CONST = '<path:filename>'

REPORTS_URL_RULE_STATIC_PATH = urljoin(REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
SWITCHING_REPORTS_URL_STATIC_PATH = urljoin(SWITCHING_REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
CONFIGURATOR_URL_STATIC_PATH = urljoin(CONFIGURATOR_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
#ENDGLOBALS

def registerServiceBlueprints(app:Flask, service_blueprints:list, service_url_prefix:str):
    for blueprint in service_blueprints:
        app.register_blueprint(blueprint, url_prefix=service_url_prefix)

def addUrlRules(app):
    app.add_url_rule(REPORTS_URL_RULE_STATIC_PATH, endpoint=REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
    app.add_url_rule(SWITCHING_REPORTS_URL_STATIC_PATH, endpoint=SWITCHING_REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
    app.add_url_rule(CONFIGURATOR_URL_STATIC_PATH, endpoint=CONFIGURATOR_URL_RULE_ENDPOINT, view_func=app.send_static_file)
