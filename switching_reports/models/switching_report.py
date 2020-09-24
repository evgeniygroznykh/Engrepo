from models.shared_db import db
from datetime import datetime as dt
from datetime import timedelta

class SwitchingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    work_type = db.Column(db.String(300), nullable=False)
    shift_comp = db.Column(db.String(300), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    translation_start_time = db.Column(db.DateTime, nullable=False)
    translation_end_time = db.Column(db.DateTime, nullable=False)
    main_source = db.Column(db.String(50), nullable=False)
    reserve_source = db.Column(db.String(50), nullable=False)
    main_destination = db.Column(db.String(50), nullable=False)
    reserve_destination = db.Column(db.String(50), nullable=False)
    customer = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text, default='Без замечаний')
    request_file_path = db.Column(db.Text)

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