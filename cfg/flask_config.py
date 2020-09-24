from flask import Flask


def registerReportServiceBlueprints(app:Flask, report_blueprints:list):
    for blueprint in report_blueprints:
        app.register_blueprint(blueprint, url_prefix='/reports')

def registerSwitchingReportServiceBlueprints(app:Flask, switching_report_blueprints:list):
    for blueprint in switching_report_blueprints:
        app.register_blueprint(blueprint, url_prefix='/switching_reports')

def addUrlRules(app):
    app.add_url_rule('/reports/static/<path:filename>', endpoint='reports/static', view_func=app.send_static_file)
    app.add_url_rule('/switching_reports/static/<path:filename>', endpoint='switching_reports/static', view_func=app.send_static_file)