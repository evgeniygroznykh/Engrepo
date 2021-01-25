from flask import render_template, request, redirect, Blueprint
from datetime import datetime as dt
from models.database_context import DatabaseContext
from switching_reports.models.translation import Translation
from switching_reports.models.switching_report import app_db
from teleport.models.teleport_record import TeleportRecord
import switching_reports.models.http_request_handler as HttpRequestHandler


TELEPORT_BLUEPRINTS = []
teleport_schedule_page = Blueprint('teleport_schedule_page', __name__, static_folder='static', template_folder='templates')
TELEPORT_BLUEPRINTS.append(teleport_schedule_page)
@teleport_schedule_page.route("/schedule/", methods=['POST', 'GET'])
@teleport_schedule_page.route("/schedule", methods=['POST', 'GET'])
def teleport_schedule():
    return render_template("teleport-schedule.html")

new_teleport_record_page = Blueprint('new_teleport_record_page', __name__, static_folder='static', template_folder='templates')
TELEPORT_BLUEPRINTS.append(new_teleport_record_page)
@new_teleport_record_page.route("/create_teleport_record/", methods=['POST', 'GET'])
@new_teleport_record_page.route("/create_teleport_record", methods=['POST', 'GET'])
def create_teleport_record():
    if request.method == 'POST':
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        service_data = request.form['teleportReportServiceData']
        teleport_record = TeleportRecord.createTeleportRecord(dt.now(), translation, service_data)

        DatabaseContext.addTeleportRecordToDatabase(app_db, teleport_record)
        return redirect('/teleport/schedule')

    else:
        return render_template("create-teleport-record.html")