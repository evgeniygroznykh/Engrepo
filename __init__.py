from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EngrepoDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = f"{os.environ['userdomain']}/{os.environ['username']}"
    summary = db.Column(db.String(300), nullable=False)
    tags = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Report %r' % self.id

@app.route("/", methods=['POST', 'GET'])
@app.route("/create-report", methods=['POST', 'GET'])
@app.route("/create-report/", methods=['POST', 'GET'])
def report():
    if not os.path.exists(os.path.join(os.getcwd(), 'EngrepoDB')):
        db.create_all()

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
        return render_template("create-report.html", user_name=user_name)

@app.route("/reports")
@app.route("/reports/")
def reports():
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template("reports.html", reports=reports)

@app.route("/reports/id=<int:id>")
def report_details(id):
    report = Report.query.get(id)
    return render_template("report-details.html", report=report)

@app.route("/reports/id=<int:id>/delete")
def report_delete(id):
    report = Report.query.get_or_404(id)

    try:
        db.session.delete(report)
        db.session.commit()
        return redirect('/reports')
    except:
        return "При удалении отчета произошла ошибка"

@app.route("/reports/id=<int:id>/update", methods=['POST', 'GET'])
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
        return render_template("report-update.html", report=report)

if __name__ == "__main__":
    app.run(debug=True)