from flask import render_template, request, redirect, Blueprint


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
    return render_template("create-teleport-record.html")