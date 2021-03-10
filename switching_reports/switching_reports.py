from switching_reports.models.switching_report import SwitchingReport, app_db
from switching_reports.models.file_handler import FileHandler
from models.database_context import DatabaseContext
from models.custom_http_response import CustomHttpResponse
from flask import render_template, request, redirect, Blueprint
from datetime import datetime as dt
from cfg.external_config import external_config
from sqlalchemy import or_, and_
from switching_reports.models.xlsx_handler import writeDataframeToXlsx, getReadableFilenameFromDates
from switching_reports.models.dataframe_handler import getDataframeFromSwitchingReports, formatDataframeForXlsxUpload
import switching_reports.models.http_request_handler as HttpRequestHandler


CUSTOMERS = external_config['customers']
WORK_TYPES = external_config['work_types']
SHIFTS = external_config['shifts']
SOURCES = external_config['sources']
DESTINATIONS = external_config['destinations']
VAR_SOURCES = external_config['var_sources']
VAR_DESTINATIONS = external_config['var_destinations']
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
                FileHandler.uploadRequestFile(UPLOAD_FOLDER, sw_report_request_file, switching_report_service_data)

        switching_report = SwitchingReport.createSwitchingReport(switching_report_service_data, translation, switching, sw_report_request_file)

        DatabaseContext.addSwitchingReportToDatabase(app_db, switching_report)
        return redirect('/switching_reports/switching_reports')

    else:
        default_translation_start_time = dt.now()
        default_translation_end_time = dt.now()
        return render_template("create-switching-report.html", work_types=WORK_TYPES, customers=CUSTOMERS,
                               shifts=SHIFTS, remarks='Без замечаний',
                               sources=SOURCES, destinations=DESTINATIONS,
                               var_sources=VAR_SOURCES, var_destinations=VAR_DESTINATIONS,
                               default_start_time=dt.strftime(default_translation_start_time, '%Y-%m-%dT%H:%M'),
                                default_end_time=dt.strftime(default_translation_end_time, '%Y-%m-%dT%H:%M'))

switching_reports_page = Blueprint('switching_reports_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_reports_page)
@switching_reports_page.route("/", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports/", methods=['POST', 'GET'])
@switching_reports_page.route("/switching_reports/sw_filter_or_download_reports", methods=['POST', 'GET'])
def get_switching_reports():
    if request.method == 'POST':
        if HttpRequestHandler.isReportingPeriodSet():
            from_date, to_date, days = HttpRequestHandler.getReportingPeriodFromFilterForm()
            time_deltas = SwitchingReport.getTimeDeltas(days)
            filtered_switching_reports = SwitchingReport.query.filter(and_(SwitchingReport.translation_start_time >= from_date,
                SwitchingReport.translation_start_time <= to_date)).order_by(SwitchingReport.translation_start_time.desc()).all()

            if HttpRequestHandler.isFilterButtonPressed():
                return render_template('switching_reports.html', switching_reports=filtered_switching_reports, work_types=WORK_TYPES,
                                        time_deltas=time_deltas, now=dt.now(), amount_of_days=days)
            elif HttpRequestHandler.isDownloadButtonPressed():
                file_name = getReadableFilenameFromDates(from_date, to_date)
                raw_dataframe = getDataframeFromSwitchingReports(filtered_switching_reports)
                formatted_dataframe = formatDataframeForXlsxUpload(raw_dataframe)
                response = CustomHttpResponse(writeDataframeToXlsx(formatted_dataframe), mimetype='application/vnd.ms-excel; charset=utf-16')
                response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
                return response
        else:
            return('', 204)
    else:
        from_date, to_date = SwitchingReport.getReportingPeriodAsTuple(REPORTING_PERIOD_IN_DAYS)
        time_deltas = SwitchingReport.getTimeDeltas(REPORTING_PERIOD_IN_DAYS)

        switching_reports = SwitchingReport.query.order_by(SwitchingReport.translation_start_time.desc()).all()
        return render_template("switching-reports.html", switching_reports=switching_reports, work_types = WORK_TYPES,
                               time_deltas=time_deltas, now=dt.now(), amount_of_days=REPORTING_PERIOD_IN_DAYS, search_string='empty',
                               default_from_value=from_date, default_to_value=to_date)

switching_report_details_page = Blueprint('switching_report_details_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(switching_report_details_page)
@switching_report_details_page.route("/switching_reports/id=<int:id>")
def get_switching_report_details(id):
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
                FileHandler.uploadRequestFile(UPLOAD_FOLDER, sw_report_request_file)
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
                                                                        shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS,
                                                                        var_sources=VAR_SOURCES, var_destinations=VAR_DESTINATIONS)

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
                                                                        .order_by(SwitchingReport.translation_start_time.desc()).all()

        return render_template('switching-reports.html', switching_reports=needed_switching_reports, work_types = WORK_TYPES, search_string=search_string)

sw_template_page = Blueprint('sw_template_page', __name__, static_folder='static', template_folder='templates')
SWITCHING_REPORT_BLUEPRINTS.append(sw_template_page)
@sw_template_page.route("/switching_reports/id=<int:id>/use_as_template", methods=['POST', 'GET'])
def use_report_as_template(id):
    switching_report = SwitchingReport.query.get_or_404(id)

    if request.method == 'POST':
        switching_report_service_data = HttpRequestHandler.getSwitchingReportServiceDataFromReqForm(is_update=False)
        sw_report_request_file = HttpRequestHandler.getRequestFileInstanceFromReqForm()
        translation = HttpRequestHandler.getTranslationInstanceFromReqForm()
        switching = HttpRequestHandler.getSwitchingInstanceFromReqForm()

        if not FileHandler.isFileInRequestForm(sw_report_request_file):
            sw_report_request_file.setFilePath(UPLOAD_FOLDER)
            if not FileHandler.isRequestFileExistsInUploadFolder(UPLOAD_FOLDER, sw_report_request_file):
                FileHandler.uploadRequestFile(UPLOAD_FOLDER, sw_report_request_file)

        switching_report = SwitchingReport.createSwitchingReport(switching_report_service_data, translation, switching,
                                                                 sw_report_request_file)

        DatabaseContext.addSwitchingReportToDatabase(app_db, switching_report)
        return redirect('/switching_reports/switching_reports')
    else:
        return render_template("switching-report-use-as-template.html", switching_report=switching_report,
                                                                        work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                        shifts=SHIFTS, sources=SOURCES, destinations=DESTINATIONS,
                                                                        var_sources=VAR_SOURCES, var_destinations=VAR_DESTINATIONS)