from models.report import db
from models.switching_report import SwitchingReport
from flask import render_template, url_for, request, redirect, Blueprint
from sqlalchemy import or_, and_
from models.dbconn import DBContext as DBC
import datetime as dt
import os
from cfg.config import CUSTOMERS, WORK_TYPES, SHIFTS, SOURCES, DESTINATIONS, UPLOAD_FOLDER

SWITCHING_REPORT_BLUEPRINTS = []
REQUEST_FILE_EXISTS_ERROR_TEXT = 'данный файл заявки уже существует, файл не был сохранён'

switching_report_page = Blueprint('switching_report_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_page)
@DBC.verify_db('Engrepo')
@switching_report_page.route("/", methods=['POST', 'GET'])
@switching_report_page.route("/create_switching_report/", methods=['POST', 'GET'])
@switching_report_page.route("/create_switching_report", methods=['POST', 'GET'])
def switching_report():
    if request.method == 'POST':
        work_type = request.form['switchingReportWorkType']
        customer = request.form['switchingCustomer']
        shift_comp = request.form['shiftComp']
        start_time = dt.datetime.strptime(request.form['translationStartTime'], '%Y-%m-%dT%H:%M')
        end_time = dt.datetime.strptime(request.form['translationEndTime'], '%Y-%m-%dT%H:%M')
        switching_source = request.form['switchingSource']
        switching_destination = request.form['switchingDestination']
        switching_reserve_source = request.form['reserveSwitchingSource']
        switching_reserve_destination = request.form['reserveSwitchingDestination']
        comment = request.form['switchingReportComment']
        remarks = request.form['switchingReportRemarks']
        request_file = request.files['requestFile']
        request_file_path = 'no request file'

        if request_file.filename != '':
            if not os.path.isfile(os.path.join(UPLOAD_FOLDER, request_file.filename)):
                request_file_path = UPLOAD_FOLDER + request_file.filename
                request_file.save(request_file_path)
            else:
                if remarks == 'Без замечаний':
                    remarks = REQUEST_FILE_EXISTS_ERROR_TEXT
                else:
                    remarks += f'; {REQUEST_FILE_EXISTS_ERROR_TEXT}'

        switching_report = SwitchingReport(work_type=work_type, customer=customer, start_time=start_time,
                                           end_time=end_time, source=switching_source, destination=switching_destination,
                                           reserve_source = switching_reserve_source, reserve_destination = switching_reserve_destination,
                                           shift_comp=shift_comp, comment=comment, remarks=remarks, request_file_path=request_file_path)

        try:
            db.session.add(switching_report)
            db.session.commit()
            return redirect('/switching_reports/switching_reports')
        except Exception as exc:
            return 'Args: %s; Error: %s;' % (exc.args, exc)
    else:
        return render_template("create-switching-report.html", work_types=WORK_TYPES, customers=CUSTOMERS, shifts=SHIFTS, remarks='Без замечаний', sources=SOURCES, destinations=DESTINATIONS)

switching_reports_page = Blueprint('switching_reports_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_reports_page)
@DBC.verify_db('Engrepo')
@switching_reports_page.route("/switching_reports", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports/", methods=['POST', 'GET'])
def switching_reports():
    switching_reports = SwitchingReport.query.order_by(SwitchingReport.date.desc()).all()
    return render_template("switching-reports.html", switching_reports=switching_reports)

switching_report_details_page = Blueprint('switching_report_details_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_details_page)
@DBC.verify_db('Engrepo')
@switching_report_details_page.route("/switching_reports/id=<int:id>")
def switching_report_details(id):
    switching_report = SwitchingReport.query.get(id)
    return render_template("switching-report-details.html", switching_report=switching_report)

switching_report_delete_page = Blueprint('switching_report_delete_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_delete_page)
@DBC.verify_db('Engrepo')
@switching_report_delete_page.route("/switching_reports/id=<int:id>/delete")
def switching_report_delete(id):
    switching_report = SwitchingReport.query.get_or_404(id)

    try:
        db.session.delete(switching_report)
        db.session.commit()
        return redirect('/switching_reports/switching_reports')
    except:
        return "При удалении отчета произошла ошибка"

switching_report_update_page = Blueprint('switching_report_update_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_update_page)
@DBC.verify_db('Engrepo')
@switching_report_update_page.route("/switching_reports/id=<int:id>/update", methods=['POST', 'GET'])
def switching_report_update(id):
    switching_report = SwitchingReport.query.get(id)

    if request.method == 'POST':
        switching_report.work_type = request.form['switchingReportWorkType']
        switching_report.customer = request.form['switchingCustomer']
        switching_report.shift_comp = request.form['shiftComp']
        switching_report.start_time = dt.datetime.strptime(request.form['translationStartTime'], '%Y-%m-%dT%H:%M')
        switching_report.end_time = dt.datetime.strptime(request.form['translationEndTime'], '%Y-%m-%dT%H:%M')
        switching_report.source = request.form['switchingSource']
        switching_report.destination = request.form['switchingDestination']
        switching_report.reserve_source = request.form['reserveSwitchingSource']
        switching_report.reserve_destination = request.form['reserveSwitchingDestination']
        switching_report.comment = request.form['switchingReportComment']
        switching_report.remarks = request.form['switchingReportRemarks']
        request_file = request.files['requestFile']

        if request_file.filename != '':
            if os.path.isfile(os.path.join(UPLOAD_FOLDER,request_file.filename)):
                if switching_report.remarks == 'Без замечаний':
                    switching_report.remarks = REQUEST_FILE_EXISTS_ERROR_TEXT
                else:
                    switching_report.remarks += f'; {REQUEST_FILE_EXISTS_ERROR_TEXT}'
            else:
                request_file.save(f'{UPLOAD_FOLDER}' + f'{request_file.filename}')
                if REQUEST_FILE_EXISTS_ERROR_TEXT in switching_report.remarks:
                    switching_report.remarks = switching_report.remarks.replace(REQUEST_FILE_EXISTS_ERROR_TEXT, '')
                    if switching_report.remarks == '':
                        switching_report.remarks = 'Без замечаний'
                if switching_report.request_file_path == 'no request file':
                    switching_report.request_file_path = ''
                switching_report.request_file_path += f'\n{UPLOAD_FOLDER}' + f'{request_file.filename}'

        try:
            db.session.commit()
            return redirect('/switching_reports/switching_reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        formatted_start_time = dt.datetime.strftime(switching_report.start_time, '%Y-%m-%dT%H:%M')
        formatted_end_time = dt.datetime.strftime(switching_report.end_time,'%Y-%m-%dT%H:%M')
        return render_template("switching-report-update.html", switching_report=switching_report,
                                                                start_time=formatted_start_time,
                                                                end_time=formatted_end_time,
                                                                work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS)

sw_search_page = Blueprint('sw_search_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_search_page)
@DBC.verify_db('Engrepo')
@sw_search_page.route("/switching_reports/sw_search", methods=['POST', 'GET'])
def sw_search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_switching_reports = SwitchingReport.query.filter(or_(SwitchingReport.work_type.ilike(f'%{search_string}%'),
                                                 SwitchingReport.comment.ilike(f'%{search_string}%'),
                                                    SwitchingReport.shift_comp.ilike(f'%{search_string}%')))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=needed_switching_reports)

sw_filter_page = Blueprint('sw_filter_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_filter_page)
@DBC.verify_db('Engrepo')
@sw_filter_page.route("/switching_reports/sw_filter_reports", methods=['POST', 'GET'])
def sw_filter_reports():
    if request.method == 'POST':
        filter_from_date = request.form['sortStartTime']
        filter_to_date = request.form['sortEndTime']

        filtered_sw_reports = SwitchingReport.query.filter(and_(SwitchingReport.date >= filter_from_date, SwitchingReport.date <= filter_to_date))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=filtered_sw_reports)