from flask import Flask, render_template
from models.shared_db import db
from reports.reports import REPORT_BLUEPRINTS
from switching_reports.switching_reports import SWITCHING_REPORT_BLUEPRINTS
from models.dbconn import DatabaseContext as DBC
from cfg.external_config import external_config
from cfg.flask_config import registerReportServiceBlueprints, registerSwitchingReportServiceBlueprints, addUrlRules

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  external_config['upload_folder']

DBC.setupApplicationDatabase(app, external_config)
DBC.initializeDatabaseAndCreateTables(db, app)

registerReportServiceBlueprints(app, REPORT_BLUEPRINTS)
registerSwitchingReportServiceBlueprints(app, SWITCHING_REPORT_BLUEPRINTS)
addUrlRules(app)

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)