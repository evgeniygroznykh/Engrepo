from models.report import Report, db
from cfg.config import get_tags
from flask import render_template, url_for, request, redirect, Blueprint
from models.dbconn import DBContext as DBC
import os

TAGS = get_tags()
BLUEPRINTS = []

report_page = Blueprint('report_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_page)
@DBC.verify_db(db)
@report_page.route("/", methods=['POST', 'GET'])
@report_page.route("/create-report", methods=['POST', 'GET'])
@report_page.route("/create-report/", methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        user_name = request.form['userName']
        report_summary = request.form['reportSummary']
        report_tags = request.form['reportTags']
        report_description = request.form['reportDescription']

        report = Report(user_name = user_name, summary = report_summary, tags = report_tags, description = report_description)
        try:
            db.session.add(report)
            db.session.commit()
            return redirect('/reports')
        except:
            return "При отправке отчета произошла ошибка"
    else:
        user_name = f"{os.environ['userdomain']}/{os.environ['username']}"
        return render_template("create-report.html", user_name=user_name, tags=TAGS)

reports_page = Blueprint('reports_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(reports_page)
@DBC.verify_db(db)
@reports_page.route("/reports", methods=['POST', 'GET'])
@reports_page.route("/reports/", methods=['POST', 'GET'])
def reports():
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template("reports.html", reports=reports, tags=TAGS)

report_details_page = Blueprint('report_details_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_details_page)
@DBC.verify_db(db)
@report_details_page.route("/reports/id=<int:id>")
def report_details(id):
    report = Report.query.get(id)
    return render_template("report-details.html", report=report)

report_delete_page = Blueprint('report_delete_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(report_delete_page)
@DBC.verify_db(db)
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
@DBC.verify_db(db)
@report_update_page.route("/reports/id=<int:id>/update", methods=['POST', 'GET'])
def report_update(id):
    report = Report.query.get(id)
    if request.method == 'POST':
        report.user_name = request.form['userName']
        report.summary = request.form['reportSummary']
        report.tags = request.form['reportTags']
        report.description = request.form['reportDescription']

        try:
            db.session.commit()
            return redirect('/reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        return render_template("report-update.html", report=report, tags=TAGS)

search_page = Blueprint('search_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(search_page)
@DBC.verify_db(db)
@search_page.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_reports = Report.query.filter(Report.summary.ilike(f'%{search_string}%'))\
                                                    .filter(Report.description.ilike(f'%{search_string}%'))\
                                                    .order_by(Report.date.desc()).all()
        return render_template('reports.html', reports=needed_reports, tags=TAGS)

search_by_tag_page = Blueprint('search_by_tag_page', __name__, static_folder='static', template_folder='template')
BLUEPRINTS.append(search_by_tag_page)
@DBC.verify_db(db)
@search_by_tag_page.route('/reports/search_by_tag', methods=['POST', 'GET'])
def search_by_tag():
    if request.method == 'POST':
        for tag in TAGS:
            if tag + '_button' in request.form.keys():
                tag_to_search = request.form[tag+'_button']
                needed_reports = Report.query.filter(Report.tags.ilike(f'%{tag_to_search}%'))\
                                                            .order_by(Report.date.desc()).all()
                return render_template('reports.html', reports=needed_reports, tags=TAGS)