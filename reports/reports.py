from reports.models.report import Report, db
from flask import render_template, request, redirect, Blueprint
from sqlalchemy import or_, and_
from cfg.external_config import external_config


TAGS = external_config['tags']
USERS = external_config['users']
REPORT_BLUEPRINTS = []

report_page = Blueprint('report_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(report_page)
@report_page.route("/", methods=['POST', 'GET'])
@report_page.route("/create_report", methods=['POST', 'GET'])
@report_page.route("/create_report/", methods=['POST', 'GET'])
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
            return redirect('/reports/reports')
        except:
            return "При отправке отчета произошла ошибка"
    else:
        return render_template("create-report.html", tags=TAGS, remarks='Без замечаний')

reports_page = Blueprint('reports_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(reports_page)
@reports_page.route("/reports", methods=['POST', 'GET'])
@reports_page.route("/reports/", methods=['POST', 'GET'])
def reports():
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template("reports.html", reports=reports, tags=TAGS)

report_details_page = Blueprint('report_details_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(report_details_page)
@report_details_page.route("/reports/id=<int:id>")
def report_details(id):
    report = Report.query.get(id)
    return render_template("report-details.html", report=report)

report_delete_page = Blueprint('report_delete_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(report_delete_page)
@report_delete_page.route("/reports/id=<int:id>/delete")
def report_delete(id):
    report = Report.query.get_or_404(id)

    try:
        db.session.delete(report)
        db.session.commit()
        return redirect('/reports/reports')
    except:
        return "При удалении отчета произошла ошибка"

report_update_page = Blueprint('report_update_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(report_update_page)
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
            return redirect('/reports/reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        return render_template("report-update.html", report=report, tags=TAGS)

search_page = Blueprint('search_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(search_page)
@search_page.route("/reports/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_reports = Report.query.filter(or_(Report.summary.ilike(f'%{search_string}%'),
                                                 Report.description.ilike(f'%{search_string}%')))\
                                                    .order_by(Report.date.desc()).all()
        return render_template('reports.html', reports=needed_reports, tags=TAGS)

search_by_tag_page = Blueprint('search_by_tag_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(search_by_tag_page)
@search_by_tag_page.route('/reports/search_by_tag', methods=['POST', 'GET'])
def search_by_tag():
    if request.method == 'POST':
        for tag in TAGS:
            if tag + '_button' in request.form.keys():
                tag_to_search = request.form[tag+'_button']
                needed_reports = Report.query.filter(Report.tags.ilike(f'%{tag_to_search}%'))\
                                                            .order_by(Report.date.desc()).all()
                return render_template('reports.html', reports=needed_reports, tags=TAGS)

filter_page = Blueprint('filter_page', __name__, static_folder='static', template_folder='templates')
REPORT_BLUEPRINTS.append(filter_page)
@filter_page.route("/reports/filter_reports", methods=['POST', 'GET'])
def filter_reports():
    if request.method == 'POST':
        filter_from_date = request.form['sortStartTime']
        filter_to_date = request.form['sortEndTime']

        filtered_reports = Report.query.filter(and_(Report.date >= filter_from_date, Report.date <= filter_to_date))\
                                        .order_by(Report.date.desc()).all()
        return render_template('reports.html', reports=filtered_reports, tags=TAGS)