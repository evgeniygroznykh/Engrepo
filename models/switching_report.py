from models.shared_db import db
from datetime import datetime


class SwitchingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    work_type = db.Column(db.String(300), nullable=False)
    shift_comp = db.Column(db.String(300), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    customer = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Switching report %r' % self.id