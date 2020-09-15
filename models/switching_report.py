from models.shared_db import db
from datetime import datetime


class SwitchingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    work_type = db.Column(db.String(300), nullable=False)
    shift_comp = db.Column(db.String(300), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(50), nullable=False)
    reserve_source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    reserve_destination = db.Column(db.String(50), nullable=False)
    customer = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text, default='Без замечаний')


    def __repr__(self):
        return '<Switching report %r' % self.id