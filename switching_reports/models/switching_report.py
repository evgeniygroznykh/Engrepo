from models.shared_db import application_database as app_db
from datetime import datetime as dt
from datetime import timedelta

class SwitchingReport(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)
    date = app_db.Column(app_db.DateTime)
    work_type = app_db.Column(app_db.String(300), nullable=False)
    shift_comp = app_db.Column(app_db.String(300), nullable=False)
    comment = app_db.Column(app_db.Text, nullable=False)
    translation_start_time = app_db.Column(app_db.DateTime, nullable=False)
    translation_end_time = app_db.Column(app_db.DateTime, nullable=False)
    main_source = app_db.Column(app_db.String(50), nullable=False)
    reserve_source = app_db.Column(app_db.String(50), nullable=False)
    main_destination = app_db.Column(app_db.String(50), nullable=False)
    reserve_destination = app_db.Column(app_db.String(50), nullable=False)
    customer = app_db.Column(app_db.String(50), nullable=False)
    remarks = app_db.Column(app_db.Text, default='Без замечаний')
    request_file_path = app_db.Column(app_db.Text)

    def __repr__(self):
        return '<Switching report %r' % self.id

    def formatTranslationStartTimeForJinja(self):
        return dt.strftime(self.translation_start_time, '%Y-%m-%dT%H:%M')

    def formatTranslationEndTimeForJinja(self):
        return dt.strftime(self.translation_end_time, '%Y-%m-%dT%H:%M')

    @staticmethod
    def formatRemarks(remarks:str, error_template:str):
        remarks = error_template if remarks == 'Без замечаний' else remarks + f'; {error_template}'

    @staticmethod
    def getReportingPeriodAsTuple(period_in_days:int):
        now = dt.now()
        default_to_value = now.__format__("%Y-%m-%dT%H:%M")
        default_from_value = (now-timedelta(days=period_in_days)).__format__("%Y-%m-%dT%H:%M")
        return (default_to_value, default_from_value)

    @staticmethod
    def getTimeDeltas(period_in_days:int):
        return [timedelta(days=i) for i in range(period_in_days)]