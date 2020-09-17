from flask import Flask, render_template
from models.shared_db import db
from reports.reports import REPORT_BLUEPRINTS
from switching_reports.switching_reports import SWITCHING_REPORT_BLUEPRINTS
from models.dbconn import DBContext as DBC
from cfg.config import UPLOAD_FOLDER, MAX_FILE_SIZE


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = MAX_FILE_SIZE

DBC.setup_db(app)
DBC.create_db(db, app)

for blueprint in REPORT_BLUEPRINTS:
    app.register_blueprint(blueprint, url_prefix='/reports')

for blueprint in SWITCHING_REPORT_BLUEPRINTS:
    app.register_blueprint(blueprint, url_prefix='/switching_reports')

app.add_url_rule('/reports/static/<path:filename>', endpoint='reports/static', view_func=app.send_static_file)
app.add_url_rule('/switching_reports/static/<path:filename>', endpoint='switching_reports/static', view_func=app.send_static_file)


@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)