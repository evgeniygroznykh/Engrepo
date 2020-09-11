from __init__ import app_database
import os
from datetime import datetime

class Report(app_database.Model):
    id = app_database.Column(app_database.Integer, primary_key=True)
    user_name = f"{os.environ['userdomain']}/{os.environ['username']}"
    summary = app_database.Column(app_database.String(300), nullable=False)
    tags = app_database.Column(app_database.Text, nullable=False)
    description = app_database.Column(app_database.Text, nullable=False)
    date = app_database.Column(app_database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Report %r' % self.id