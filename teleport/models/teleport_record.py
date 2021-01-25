from models.shared_db import application_database as app_db
from switching_reports.models.translation import Translation


class TeleportRecord(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)
    creation_date = app_db.Column(app_db.DateTime)
    modified_date = app_db.Column(app_db.DateTime)
    sat_start_time = app_db.Column(app_db.DateTime)
    sat_end_time = app_db.Column(app_db.DateTime)
    service_data = app_db.Column(app_db.Text)

    def __repr__(self):
        return '<Switching report %r' % self.id

    def to_dict(self):
        return {
            'Creation date':self.creation_date,
            'Modified date':self.modified_date,
            'Satellite start time':self.sat_start_time,
            'Satellite end time':self.sat_end_time
        }

    @staticmethod
    def createTeleportRecord(creation_date, translation:Translation, service_data, modified_date=None):
        return TeleportRecord(creation_date=creation_date,
                                modified_date=modified_date,
                                    sat_start_time=translation.stringifyStartTime(),
                                        sat_end_time=translation.stringifyEndTime(),
                                            service_data=service_data)
