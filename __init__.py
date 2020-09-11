from flask import Flask, render_template, url_for, request, redirect
from models.dbconn import DBContext as DBC
import models.report
import os
import json

#GLOBAL
with open('cfg/config.json', 'r', encoding='utf-8') as read_json_config:
    tags_json = json.load(read_json_config)
TAGS = tags_json['tags']
#ENDGLOBAL

app = Flask(__name__)

DBC.setup_db(app)
app_database = DBC.create_db(app)

@DBC.verify_db(app_database)
@app.route("/", methods=['POST', 'GET'])
@app.route("/create-report", methods=['POST', 'GET'])
@app.route("/create-report/", methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        user_name = request.form['userName']
        report_summary = request.form['reportSummary']
        report_tags = request.form['reportTags']
        report_description = request.form['reportDescription']

        report = models.report.Report(user_name = user_name, summary = report_summary, tags = report_tags, description = report_description)
        try:
            app_database.session.add(report)
            app_database.session.commit()
            return redirect('/reports')
        except:
            return "При отправке отчета произошла ошибка"
    else:
        user_name = f"{os.environ['userdomain']}/{os.environ['username']}"
        return render_template("create-report.html", user_name=user_name, tags=TAGS)

@DBC.verify_db(app_database)
@app.route("/reports", methods=['POST', 'GET'])
@app.route("/reports/", methods=['POST', 'GET'])
def reports():
    reports = models.report.Report.query.order_by(models.report.Report.date.desc()).all()
    return render_template("reports.html", reports=reports, tags=TAGS)

@DBC.verify_db(app_database)
@app.route("/reports/id=<int:id>")
def report_details(id):
    report = models.report.Report.query.get(id)
    return render_template("report-details.html", report=report)

@DBC.verify_db(app_database)
@app.route("/reports/id=<int:id>/delete")
def report_delete(id):
    report = models.report.Report.query.get_or_404(id)

    try:
        app_database.session.delete(report)
        app_database.session.commit()
        return redirect('/reports')
    except:
        return "При удалении отчета произошла ошибка"

@DBC.verify_db(app_database)
@app.route("/reports/id=<int:id>/update", methods=['POST', 'GET'])
def report_update(id):
    report = models.report.Report.query.get(id)
    if request.method == 'POST':
        report.user_name = request.form['userName']
        report.summary = request.form['reportSummary']
        report.tags = request.form['reportTags']
        report.description = request.form['reportDescription']

        try:
            app_database.session.commit()
            return redirect('/reports')
        except:
            return "При обновлении отчета произошла ошибка"
    else:
        return render_template("report-update.html", report=report, tags=TAGS)

@DBC.verify_db(app_database)
@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_string = request.form['search_string']
        needed_reports = models.report.Report.query.filter(models.report.Report.summary.ilike(f'%{search_string}%'))\
                                                    .filter(models.report.Report.description.ilike(f'%{search_string}%'))\
                                                    .order_by(models.report.Report.date.desc()).all()
        return render_template('reports.html', reports=needed_reports, tags=TAGS)

@DBC.verify_db(app_database)
@app.route('/reports/search_by_tag', methods=['POST', 'GET'])
def search_by_tag():
    if request.method == 'POST':
        for tag in TAGS:
            if tag + '_button' in request.form.keys():
                tag_to_search = request.form[tag+'_button']
                needed_reports = models.report.Report.query.filter(models.report.Report.tags.ilike(f'%{tag_to_search}%'))\
                                                            .order_by(models.report.Report.date.desc()).all()
                return render_template('reports.html', reports=needed_reports, tags=TAGS)

if __name__ == "__main__":
    app.run(debug=True)