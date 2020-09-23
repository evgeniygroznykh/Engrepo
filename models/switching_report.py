from models.shared_db import db
from datetime import datetime as dt


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

    def formatTranslationEndTimeForJinja(self):
        return dt.strftime(self.translation_start_time, '%Y-%m-%dT%H:%M')

    def formatTranslationEndTimeForJinja(self):
        return dt.strftime(self.translation_end_time, '%Y-%m-%dT%H:%M')