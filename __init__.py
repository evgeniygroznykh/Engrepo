from flask import Flask, render_template
from models.shared_db import application_database
from models.database_context import DatabaseContext as DBC
from cfg.external_config import external_config
from cfg.flask_config import addUrlRules, registerServiceBlueprints
from reports.reports import REPORT_BLUEPRINTS
from switching_reports.switching_reports import SWITCHING_REPORT_BLUEPRINTS
from configurator.configurator import CONFIGURATOR_BLUEPRINTS


#GLOBALS
REPORTS_URL_PREFIX = '/reports'
SWITCHING_REPORTS_URL_PREFIX = '/switching_reports'
CONFIGURATOR_URL_PREFIX = '/'

SERVICE_URL_PREFIX_DICT = {
    REPORTS_URL_PREFIX : REPORT_BLUEPRINTS,
    SWITCHING_REPORTS_URL_PREFIX : SWITCHING_REPORT_BLUEPRINTS,
    CONFIGURATOR_URL_PREFIX :  CONFIGURATOR_BLUEPRINTS
}
#ENDGLOBALS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = external_config['upload_folder']

DBC.setupApplicationDatabase(app, external_config)
DBC.initializeDatabaseAndCreateTables(application_database, app)

for service_url_prefix in SERVICE_URL_PREFIX_DICT.keys():
    registerServiceBlueprints(app, SERVICE_URL_PREFIX_DICT[service_url_prefix], service_url_prefix)
addUrlRules(app)



@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
