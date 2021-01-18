from flask import Flask, render_template
from models.shared_db import application_database
from models.database_context import DatabaseContext as DBC
from cfg.external_config import external_config
from cfg.flask_config import registerServiceBlueprints, addUrlRules, REPORTS_URL_PREFIX, \
                                                            SWITCHING_REPORTS_URL_PREFIX, \
                                                                TELEPORT_SCHEDULE_URL_PREFIX
from reports.reports import REPORT_BLUEPRINTS
from switching_reports.switching_reports import SWITCHING_REPORT_BLUEPRINTS
from teleport.teleport_records import TELEPORT_BLUEPRINTS


#GLOBALS
ENDPOINTS_DICT = {REPORTS_URL_PREFIX:REPORT_BLUEPRINTS,
                  SWITCHING_REPORTS_URL_PREFIX:SWITCHING_REPORT_BLUEPRINTS,
                  TELEPORT_SCHEDULE_URL_PREFIX:TELEPORT_BLUEPRINTS}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = external_config['upload_folder']

DBC.setupApplicationDatabase(app, external_config)
DBC.initializeDatabaseAndCreateTables(application_database, app)

for prefix, blueprint_list in ENDPOINTS_DICT.items():
    registerServiceBlueprints(app, blueprint_list, prefix)
addUrlRules(app)


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
