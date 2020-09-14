from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(300), nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    tags = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Report %r' % self.id