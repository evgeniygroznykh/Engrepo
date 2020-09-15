from models.report import Report, db
from models.switching_report import SwitchingReport
from cfg.config import get_tags, get_users, get_work_types, get_shifts, get_customers
from flask import render_template, url_for, request, redirect, Blueprint
from sqlalchemy import or_, and_
from models.dbconn import DBContext as DBC
import datetime as dt

TAGS = get_tags()
CUSTOMERS = get_customers()
USERS = get_users()
SHIFTS = get_shifts()
WORK_TYPES = get_work_types()
BLUEPRINTS = []

report_page = Blueprint('report_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_page)
@DBC.verify_db('Engrepo')
@report_page.route("/", methods=['POST', 'GET'])
@report_page.route("/create-report", methods=['POST', 'GET'])
@report_page.route("/create-report/", methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        user_name = request.form['userName']
        summary = request.form['reportSummary']
        tags = request.form['reportTags']
        description = request.form['reportDescription']
        remarks = request.form['reportRemarks']

        report = Report(user_name = USERS[user_name.lower().title()] if user_name.lower().title() in USERS.keys()
                                                                    else user_name, summary = summary,
                                                                                        tags = tags,
                                                                                        description = description,
                                                                                        remarks = remarks)
        try:
            db.session.add(report)
            db.session.commit()
            return redirect('/reports')
        except:
            return "При отправке отчета произошла ошибка"
    else:
        return render_template("create-report.html", tags=TAGS, remarks='Без замечаний')

reports_page = Blueprint('reports_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(reports_page)
@DBC.verify_db('Engrepo')
@reports_page.route("/reports", methods=['POST', 'GET'])
@reports_page.route("/reports/", methods=['POST', 'GET'])
def reports():
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template("reports.html", reports=reports, tags=TAGS)

report_details_page = Blueprint('report_details_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_details_page)
@DBC.verify_db('Engrepo')
@report_details_page.route("/reports/id=<int:id>")
def report_details(id):
    report = Report.query.get(id)
    return render_template("report-details.html", report=report)

report_delete_page = Blueprint('report_delete_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_delete_page)
@DBC.verify_db('Engrepo')
@report_delete_page.route("/reports/id=<int:id>/delete")
def report_delete(id):
    report = Report.query.get_or_404(id)

    try:
        db.session.delete(report)
        db.session.commit()
        return redirect('/reports')
    except:
        return "При удалении отчета произошла ошибка"

report_update_page = Blueprint('report_update_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_update_page)
@DBC.verify_db('Engrepo')
@report_update_page.route("/reports/id=<int:id>/update", methods=['POST', 'GET'])
def report_update(id):
    report = Report.query.get(id)
    if request.method == 'POST':
        report.user_name = request.form['userName']
        report.summary = request.form['reportSummary']
        report.tags = request.form['reportTags']
        report.description = request.form['reportDescription']
        report.remarks = request.form['reportRemarks']

        try:
            db.session.commit()
            return redirect('/reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        return render_template("report-update.html", report=report, tags=TAGS)

switching_report_page = Blueprint('switching_report_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(switching_report_page)
@DBC.verify_db('Engrepo')
@switching_report_page.route("/create-switching-report/", methods=['POST', 'GET'])
@switching_report_page.route("/create-switching-report", methods=['POST', 'GET'])
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

        switching_report = SwitchingReport(work_type=work_type, customer=customer, start_time=start_time,
                                           end_time=end_time, source=switching_source, destination=switching_destination,
                                           reserve_source = switching_reserve_source, reserve_destination = switching_reserve_destination,
                                           shift_comp=shift_comp, comment=comment, remarks=remarks)

        try:
            db.session.add(switching_report)
            db.session.commit()
            return redirect('/switching-reports')
        except Exception as exc:
            return 'Args: %s; Error: %s;' % (exc.args, exc)
    else:
        return render_template("create-switching-report.html", work_types=WORK_TYPES, customers=CUSTOMERS, shifts=SHIFTS, remarks='Без замечаний')

switching_reports_page = Blueprint('switching_reports_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(switching_reports_page)
@DBC.verify_db('Engrepo')
@switching_reports_page.route("/switching-reports", methods=['POST', 'GET'])
@switching_reports_page.route("/switching-reports/", methods=['POST', 'GET'])
def switching_reports():
    switching_reports = SwitchingReport.query.order_by(SwitchingReport.date.desc()).all()
    return render_template("switching-reports.html", switching_reports=switching_reports)

switching_report_details_page = Blueprint('switching_report_details_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(switching_report_details_page)
@DBC.verify_db('Engrepo')
@switching_report_details_page.route("/switching-reports/id=<int:id>")
def switching_report_details(id):
    switching_report = SwitchingReport.query.get(id)
    return render_template("switching-report-details.html", switching_report=switching_report)

switching_report_delete_page = Blueprint('switching_report_delete_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(switching_report_delete_page)
@DBC.verify_db('Engrepo')
@switching_report_delete_page.route("/switching-reports/id=<int:id>/delete")
def switching_report_delete(id):
    switching_report = SwitchingReport.query.get_or_404(id)

    try:
        db.session.delete(switching_report)
        db.session.commit()
        return redirect('/switching-reports')
    except:
        return "При удалении отчета произошла ошибка"

switching_report_update_page = Blueprint('switching_report_update_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(switching_report_update_page)
@DBC.verify_db('Engrepo')
@switching_report_update_page.route("/switching-reports/id=<int:id>/update", methods=['POST', 'GET'])
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

        try:
            db.session.commit()
            return redirect('/switching-reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        formatted_start_time = dt.datetime.strftime(switching_report.start_time, '%Y-%m-%dT%H:%M')
        formatted_end_time = dt.datetime.strftime(switching_report.end_time,'%Y-%m-%dT%H:%M')
        return render_template("switching-report-update.html", switching_report=switching_report,
                                                                start_time=formatted_start_time,
                                                                end_time=formatted_end_time,
                                                                work_types=WORK_TYPES, customers=CUSTOMERS,
                                                                shifts=SHIFTS)

search_page = Blueprint('search_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(search_page)
@DBC.verify_db('Engrepo')
@search_page.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_reports = Report.query.filter(or_(Report.summary.ilike(f'%{search_string}%'),
                                                 Report.description.ilike(f'%{search_string}%')))\
                                                    .order_by(Report.date.desc()).all()
        return render_template('reports.html', reports=needed_reports, tags=TAGS)

search_by_tag_page = Blueprint('search_by_tag_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(search_by_tag_page)
@DBC.verify_db('Engrepo')
@search_by_tag_page.route('/reports/search_by_tag', methods=['POST', 'GET'])
def search_by_tag():
    if request.method == 'POST':
        for tag in TAGS:
            if tag + '_button' in request.form.keys():
                tag_to_search = request.form[tag+'_button']
                needed_reports = Report.query.filter(Report.tags.ilike(f'%{tag_to_search}%'))\
                                                            .order_by(Report.date.desc()).all()
                return render_template('reports.html', reports=needed_reports, tags=TAGS)

sw_search_page = Blueprint('sw_search_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(sw_search_page)
@DBC.verify_db('Engrepo')
@sw_search_page.route("/sw_search", methods=['POST', 'GET'])
def sw_search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_switching_reports = SwitchingReport.query.filter(or_(SwitchingReport.work_type.ilike(f'%{search_string}%'),
                                                 SwitchingReport.comment.ilike(f'%{search_string}%'),
                                                    SwitchingReport.shift_comp.ilike(f'%{search_string}%')))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=needed_switching_reports)

filter_page = Blueprint('filter_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(filter_page)
@DBC.verify_db('Engrepo')
@filter_page.route("/filter_reports", methods=['POST', 'GET'])
def filter_reports():
    if request.method == 'POST':
        filter_from_date = request.form['sortStartTime']
        filter_to_date = request.form['sortEndTime']

        filtered_reports = Report.query.filter(and_(Report.date >= filter_from_date, Report.date <= filter_to_date))\
                                        .order_by(Report.date.desc()).all()
        return render_template('reports.html', reports=filtered_reports, tags=TAGS)


sw_filter_page = Blueprint('sw_filter_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(sw_filter_page)
@DBC.verify_db('Engrepo')
@sw_filter_page.route("/sw_filter_reports", methods=['POST', 'GET'])
def sw_filter_reports():
    if request.method == 'POST':
        filter_from_date = request.form['sortStartTime']
        filter_to_date = request.form['sortEndTime']

        filtered_sw_reports = SwitchingReport.query.filter(and_(SwitchingReport.date >= filter_from_date, SwitchingReport.date <= filter_to_date))\
                                                    .order_by(SwitchingReport.date.desc()).all()
        return render_template('switching-reports.html', switching_reports=filtered_sw_reports)