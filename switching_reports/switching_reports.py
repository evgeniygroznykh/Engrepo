from switching_reports.models.switching_report import SwitchingReport, app_db
from switching_reports.models.http_request_handler import HttpRequestHandler
from switching_reports.models.file_handler import FileHandler
from models.database_context import DatabaseContext
from models.custom_http_response import CustomHttpResponse
from flask import render_template, request, redirect, Blueprint
from datetime import datetime as dt
from cfg.external_config import external_config
from sqlalchemy import or_, and_
from switching_reports.models.csv_handler import getDataframeFromSwitchingReports, writeDataframeToCsv, getReadableFilenameFromDates


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
        switching_report_service_data = HttpRequestHandler.getSwitchingReportServiceDataFromReqForm(is_update=False)
        sw_report_request_file = HttpRequestHandler.getRequestFileInstanceFromReqForm()
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        switching = HttpRequestHandler.getSwitchingInstanceFromReqForm()

        if not FileHandler.isFileInRequestForm(sw_report_request_file):
            sw_report_request_file.setFilePath(UPLOAD_FOLDER)
            if not FileHandler.isRequestFileExistsInUploadFolder(UPLOAD_FOLDER, sw_report_request_file):
                FileHandler.uploadRequestFile(sw_report_request_file)

        switching_report = SwitchingReport(creation_date=switching_report_service_data.creation_date, work_type=switching_report_service_data.work_type, customer=switching_report_service_data.customer,
                                           translation_start_time=translation.stringifyStartTime(), translation_end_time=translation.stringifyEndTime(),
                                           main_source=switching.main_source, main_destination = switching.main_destination,
                                           reserve_source=switching.reserve_source, reserve_destination=switching.reserve_destination,
                                           shift_comp=switching_report_service_data.shift_composition, comment=switching_report_service_data.comment,
                                           remarks=switching_report_service_data.remarks, request_file_path=sw_report_request_file.request_file_path)

        DatabaseContext.addSwitchingReportToDatabase(app_db, switching_report)
        return redirect('/switching_reports/switching_reports')

    else:
        default_translation_start_time = dt.now()
        default_translation_end_time = dt.now()
        return render_template("create-switching-report.html", work_types=WORK_TYPES, customers=CUSTOMERS,
                               shifts=SHIFTS, remarks='Без замечаний',
                               sources=SOURCES, destinations=DESTINATIONS,
                               default_start_time=dt.strftime(default_translation_start_time, '%Y-%m-%dT%H:%M'),
                                default_end_time=dt.strftime(default_translation_end_time, '%Y-%m-%dT%H:%M'))

switching_reports_page = Blueprint('switching_reports_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_reports_page)
@switching_report_page.route("/", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports/", methods=['POST', 'GET'])
def switching_reports():
    reporting_period = SwitchingReport.getReportingPeriodAsTuple(REPORTING_PERIOD_IN_DAYS)
    reporting_from, reporting_to = reporting_period
    time_deltas = SwitchingReport.getTimeDeltas(REPORTING_PERIOD_IN_DAYS)

    switching_reports = SwitchingReport.query.order_by(SwitchingReport.creation_date.desc()).all()
    return render_template("switching-reports.html", switching_reports=switching_reports, work_types = WORK_TYPES,
                           time_deltas=time_deltas, now=dt.now(), amount_of_days=REPORTING_PERIOD_IN_DAYS, search_string='empty',
                           default_from_value = reporting_from, default_to_value = reporting_to)

switching_report_details_page = Blueprint('switching_report_details_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_details_page)
@switching_report_details_page.route("/switching_reports/id=<int:id>")
def switching_report_details(id):
    switching_report = SwitchingReport.query.get_or_404(id)
    return render_template("switching-report-details.html", switching_report=switching_report)

switching_report_delete_page = Blueprint('switching_report_delete_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_delete_page)
@switching_report_delete_page.route("/switching_reports/id=<int:id>/delete")
def switching_report_delete(id):
    switching_report = SwitchingReport.query.get_or_404(id)
    DatabaseContext.deleteSwitchingReportFromDatabase(app_db, switching_report)
    return redirect('/switching_reports/switching_reports')

switching_report_update_page = Blueprint('switching_report_update_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_update_page)
@switching_report_update_page.route("/switching_reports/id=<int:id>/update", methods=['POST', 'GET'])
def switching_report_update(id):
    switching_report = SwitchingReport.query.get_or_404(id)

    if request.method == 'POST':
        switching_report_service_data = HttpRequestHandler.getSwitchingReportServiceDataFromReqForm(is_update=True, switching_report=switching_report)
        sw_report_request_file = HttpRequestHandler.getRequestFileInstanceFromReqForm()
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        switching = HttpRequestHandler.getSwitchingInstanceFromReqForm()

        if not FileHandler.isFileInRequestForm(sw_report_request_file):
            sw_report_request_file.setFilePath(UPLOAD_FOLDER)
            if not FileHandler.isRequestFileExistsInUploadFolder(UPLOAD_FOLDER, sw_report_request_file):
                FileHandler.uploadRequestFile(sw_report_request_file)
                switching_report.updateRequestFilePath(sw_report_request_file)
                switching_report.formatRemarksIfNoRemarks()

        switching_report.updateServiceData(switching_report_service_data)
        switching_report.updateTranslationData(translation)
        switching_report.updateSwitchingData(switching)

        DatabaseContext.databaseSessionCommitChanges(app_db)
        return redirect('/switching_reports/switching_reports')
    else:
        return render_template("switching-report-update.html", switching_report=switching_report,
                                                                        work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                        shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS)

sw_search_page = Blueprint('sw_search_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_search_page)
@sw_search_page.route("/switching_reports/sw_search", methods=['POST', 'GET'])
def switching_report_search():
    if request.method == 'POST':
        search_string = HttpRequestHandler.getSearchStringFromSearchForm()

        needed_switching_reports = SwitchingReport.query.filter(or_(SwitchingReport.work_type.ilike(f'%{search_string}%'),
                                                                   SwitchingReport.comment.ilike(f'%{search_string}%'),
                                                                   SwitchingReport.shift_comp.ilike(
                                                                       f'%{search_string}%'))) \
                                                                        .order_by(SwitchingReport.creation_date.desc()).all()

        return render_template('switching-reports.html', switching_reports=needed_switching_reports, work_types = WORK_TYPES, search_string=search_string)

sw_filter_page = Blueprint('sw_filter_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_filter_page)
@sw_filter_page.route("/switching_reports/sw_filter_reports", methods=['POST', 'GET'])
def switching_reports_filter():
    if request.method == 'POST':
        if 'filter_button' in request.form:
            if not HttpRequestHandler.getReportingPeriodFromFilterForm() == None:
                filter_from_date, filter_to_date, days = HttpRequestHandler.getReportingPeriodFromFilterForm()
                time_deltas = SwitchingReport.getTimeDeltas(days)

                filtered_switching_reports = SwitchingReport.query.filter(
                    and_(SwitchingReport.creation_date >= filter_from_date, SwitchingReport.creation_date <= filter_to_date)) \
                    .order_by(SwitchingReport.creation_date.desc()).all()

                return render_template('switching-reports.html', switching_reports=filtered_switching_reports, work_types = WORK_TYPES,
                                                                    time_deltas=time_deltas, now=dt.now(), amount_of_days=days, search_string='empty')
            else:
                return ('', 204)
        if 'download_button' in request.form:
            if not HttpRequestHandler.getReportingPeriodFromFilterForm() == None:
                from_date, to_date, days = HttpRequestHandler.getReportingPeriodFromFilterForm()
                filtered_switching_reports = SwitchingReport.query.filter(
                    and_(SwitchingReport.creation_date >= from_date, SwitchingReport.creation_date <= to_date)) \
                    .order_by(SwitchingReport.creation_date.desc()).all()

                file_name = getReadableFilenameFromDates(from_date, to_date)
                dataframe = getDataframeFromSwitchingReports(filtered_switching_reports)
                response = CustomHttpResponse(writeDataframeToCsv(dataframe), mimetype='text/csv; charset=utf-16')
                response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
                return response
            else:
                return ('', 204)

sw_template_page = Blueprint('sw_template_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_template_page)
@sw_template_page.route("/switching_reports/id=<int:id>/use_as_template", methods=['POST', 'GET'])
def use_as_template(id):
    switching_report = SwitchingReport.query.get_or_404(id)

    if request.method == 'POST':
        switching_report_service_data = HttpRequestHandler.getSwitchingReportServiceDataFromReqForm()
        sw_report_request_file = HttpRequestHandler.getRequestFileInstanceFromReqForm()
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        switching = HttpRequestHandler.getSwitchingInstanceFromReqForm()

        if not FileHandler.isFileInRequestForm(sw_report_request_file):
            sw_report_request_file.setFilePath(UPLOAD_FOLDER)
            if not FileHandler.isRequestFileExistsInUploadFolder(UPLOAD_FOLDER, sw_report_request_file):
                FileHandler.uploadRequestFile(sw_report_request_file)

        switching_report = SwitchingReport(creation_date=dt.now(),
                                           work_type=switching_report_service_data.work_type,
                                           customer=switching_report_service_data.customer,
                                           translation_start_time=translation.stringifyStartTime(),
                                           translation_end_time=translation.stringifyEndTime(),
                                           main_source=switching.main_source,
                                           main_destination=switching.main_destination,
                                           reserve_source=switching.reserve_source,
                                           reserve_destination=switching.reserve_destination,
                                           shift_comp=switching_report_service_data.shift_composition,
                                           comment=switching_report_service_data.comment,
                                           remarks=switching_report_service_data.remarks,
                                           request_file_path=sw_report_request_file.request_file_path)

        DatabaseContext.addSwitchingReportToDatabase(app_db, switching_report)
        return redirect('/switching_reports/switching_reports')
    else:
        return render_template("switching-report-use-as-template.html", switching_report=switching_report,
                                                                        work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                        shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS)