from urllib.parse import urljoin
from flask import Flask


#GLOBALS
REPORTS_URL_PREFIX = '/reports'
SWITCHING_REPORTS_URL_PREFIX = '/switching_reports'

REPORTS_URL_RULE_ENDPOINT = '/reports/static/'
SWITCHING_REPORTS_URL_RULE_ENDPOINT = '/switching_reports/static/'

PATH_FILE_NAME_CONST = '<path:filename>'

REPORTS_URL_RULE_STATIC_PATH = urljoin(REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
SWITCHING_REPORTS_URL_STATIC_PATH = urljoin(SWITCHING_REPORTS_URL_RULE_ENDPOINT, PATH_FILE_NAME_CONST)
#ENDGLOBALS

def registerReportServiceBlueprints(app:Flask, report_blueprints:list):
    for blueprint in report_blueprints:
        app.register_blueprint(blueprint, url_prefix=REPORTS_URL_PREFIX)

def registerSwitchingReportServiceBlueprints(app:Flask, switching_report_blueprints:list):
    for blueprint in switching_report_blueprints:
        app.register_blueprint(blueprint, url_prefix=SWITCHING_REPORTS_URL_PREFIX)

def addUrlRules(app):
    app.add_url_rule(REPORTS_URL_RULE_STATIC_PATH, endpoint=REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
    app.add_url_rule(SWITCHING_REPORTS_URL_STATIC_PATH, endpoint=SWITCHING_REPORTS_URL_RULE_ENDPOINT, view_func=app.send_static_file)
