from switching_reports.models.switching_report import SwitchingReport, db
from switching_reports.models.translation import Translation
from switching_reports.models.switching import Switching
from switching_reports.models.http_request_handler import HttpRequestHandler
from switching_reports.models.file_handler import FileHandler
from models.dbconn import DatabaseContext
from flask import render_template, request, redirect, Blueprint
from sqlalchemy import or_, and_
from datetime import datetime as dt
from datetime import timedelta
import os
from cfg.external_config import external_config


CUSTOMERS = external_config['customers']
WORK_TYPES = external_config['work_types']
SHIFTS = external_config['shifts']
SOURCES = external_config['sources']
DESTINATIONS = external_config['destinations']
UPLOAD_FOLDER = external_config['upload_folder']
REQUEST_FILE_EXISTS_ERROR_TEXT = external_config['file_exists_error_template']
REPORTING_PERIOD_IN_DAYS = external_config['reporting_period_in_days']

SWITCHING_REPORT_BLUEPRINTS = []

switching_report_page = Blueprint('switching_report_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_page)
@switching_report_page.route("/create_switching_report/", methods=['POST', 'GET'])
@switching_report_page.route("/create_switching_report", methods=['POST', 'GET'])
def create_switching_report():
    if request.method == 'POST':
        switching_report_service_data = HttpRequestHandler.getSwitchingReportServiceDataFromReqForm()
        sw_report_request_file = HttpRequestHandler.getRequestFileInstanceFromReqForm()
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        switching = HttpRequestHandler.getSwitchingInstanceFromReqForm()

        if not FileHandler.isFileInRequestForm(sw_report_request_file):
            if not FileHandler.isRequestFileExists(sw_report_request_file):
                FileHandler.uploadRequestFile(sw_report_request_file)
        else:
            SwitchingReport.formatRemarks(switching_report_service_data.remarks, REQUEST_FILE_EXISTS_ERROR_TEXT)

        switching_report = SwitchingReport(date=switching_report_service_data.date, work_type=switching_report_service_data.work_type, customer=switching_report_service_data.customer,
                                           translation_start_time=translation.stringifyStartTime(), translation_end_time=translation.stringifyEndTime(),
                                           main_source=switching.main_source, main_destination = switching.main_destination,
                                           reserve_source=switching.reserve_source, reserve_destination=switching.reserve_destination,
                                           shift_comp=switching_report_service_data.shift_composition, comment=switching_report_service_data.comment,
                                           remarks=switching_report_service_data.remarks, request_file_path=sw_report_request_file.request_file_path)

        DatabaseContext.addSwitchingReportToDatabase(db, switching_report)
        return redirect('/switching_reports/switching_reports')

    else:
        return render_template("create-switching-report.html", work_types=WORK_TYPES, customers=CUSTOMERS, shifts=SHIFTS, remarks='Без замечаний', sources=SOURCES, destinations=DESTINATIONS)

switching_reports_page = Blueprint('switching_reports_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_reports_page)
@switching_report_page.route("/", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports/", methods=['POST', 'GET'])
def switching_reports():
    reporting_period = SwitchingReport.getReportingPeriodAsTuple(REPORTING_PERIOD_IN_DAYS)
    reporting_from, reporting_to = reporting_period
    time_deltas = SwitchingReport.getTimeDeltas(REPORTING_PERIOD_IN_DAYS)

    switching_reports = SwitchingReport.query.order_by(SwitchingReport.date.desc()).all()
    return render_template("switching-reports.html", switching_reports=switching_reports, work_types = WORK_TYPES,
                           time_deltas=time_deltas, now=dt.now(), amount_of_days=14, search_string='empty',
                           default_from_value = reporting_from, default_to_value = reporting_to)

switching_report_details_page = Blueprint('switching_report_details_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_details_page)
@switching_report_details_page.route("/switching_reports/id=<int:id>")
def switching_report_details(id):
    switching_report = SwitchingReport.query.get(id)
    return render_template("switching-report-details.html", switching_report=switching_report)

switching_report_delete_page = Blueprint('switching_report_delete_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_delete_page)
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
@switching_report_update_page.route("/switching_reports/id=<int:id>/update", methods=['POST', 'GET'])
def switching_report_update(id):
    switching_report = SwitchingReport.query.get(id)

    if request.method == 'POST':
        switching_report.date = dt.now()
        switching_report.work_type = request.form['switchingReportWorkType']
        switching_report.customer = request.form['switchingCustomer']
        switching_report.shift_comp = request.form['shiftComp']

        start_time = dt.strptime(request.form['translationStartTime'], '%Y-%m-%dT%H:%M')
        end_time = dt.strptime(request.form['translationEndTime'], '%Y-%m-%dT%H:%M')
        translation = Translation(start_time, end_time)
        switching_report.translation_start_time, switching_report.translation_end_time = translation.start_time, translation.end_time

        switching_source = request.form['switchingSource']
        switching_destination = request.form['switchingDestination']
        switching_reserve_source = request.form['reserveSwitchingSource']
        switching_reserve_destination = request.form['reserveSwitchingDestination']
        switching = Switching(switching_source, switching_destination, switching_reserve_source,
                              switching_reserve_destination)
        switching_report.main_source, switching_report.main_destination  = switching.main_source, switching.main_destination
        switching_report.reserve_source, switching_report.reserve_destination = switching.reserve_source, switching.reserve_destination

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
        return render_template("switching-report-update.html", switching_report=switching_report,
                                                                        work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                        shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS)

sw_search_page = Blueprint('sw_search_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_search_page)
@sw_search_page.route("/switching_reports/sw_search", methods=['POST', 'GET'])
def sw_search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_switching_reports = SwitchingReport.query.filter(or_(SwitchingReport.work_type.ilike(f'%{search_string}%'),
                                                 SwitchingReport.comment.ilike(f'%{search_string}%'),
                                                    SwitchingReport.shift_comp.ilike(f'%{search_string}%')))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=needed_switching_reports, work_types = WORK_TYPES, search_string=search_string)

sw_filter_page = Blueprint('sw_filter_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_filter_page)
@sw_filter_page.route("/switching_reports/sw_filter_reports", methods=['POST', 'GET'])
def sw_filter_reports():
    if request.method == 'POST':
        filter_from_date = dt.datetime.strptime(request.form['sortStartTime'], '%Y-%m-%dT%H:%M')
        filter_to_date = dt.datetime.strptime(request.form['sortEndTime'], '%Y-%m-%dT%H:%M')
        days = (filter_to_date - filter_from_date).days

        time_deltas = [dt.timedelta(days=i) for i in range(days)]

        filtered_sw_reports = SwitchingReport.query.filter(and_(SwitchingReport.date >= filter_from_date, SwitchingReport.date <= filter_to_date))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=filtered_sw_reports, work_types = WORK_TYPES,
                                                            time_deltas=time_deltas, now=dt.datetime.now(), amount_of_days=days, search_string='empty')