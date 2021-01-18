from models.shared_db import application_database as app_db


class TeleportRecord(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)

    #Teleport record timings
    creation_date = app_db.Column(app_db.DateTime)
    modified_date = app_db.Column(app_db.DateTime)
    sat_start_time = app_db.Column(app_db.DateTime)
    sat_end_time = app_db.Column(app_db.DateTime)
    pgm_start_time = app_db.Column(app_db.DateTime)

    #Configuration
    aspect_ratio = app_db.Column(app_db.String(25))
    production_standard = app_db.Column(app_db.String(50))
    distribution_standard = app_db.Column(app_db.String(50))
    signal_description = app_db.Column(app_db.Text)
    graphics_language = app_db.Column(app_db.String(50))
    satellite = app_db.Column(app_db.String(100))
    satellite_txp_ch = app_db.Column(app_db.Text)
    satellite_access_number = app_db.Column(app_db.String(50))
    u_l_frequency = app_db.Column(app_db.String(50))
    u_l_polarization = app_db.Column(app_db.String(5))
    d_l_frequency = app_db.Column(app_db.String(50))
    d_l_polarization = app_db.Column(app_db.String(5))
    fec = app_db.Column(app_db.String(5))
    symbol = app_db.Column(app_db.String(25))
    modulation = app_db.Column(app_db.String(50))
    mpeg_codec = app_db.Column(app_db.String(25))
    encryption_biss = app_db.Column(app_db.String(25))
    encryption_code = app_db.Column(app_db.String(100))
    pilot_tones = app_db.Column(app_db.String(5))
    rolloff = app_db.Column(app_db.String(5))
    audio_configuration = app_db.Text(app_db.Text)

    #Service data
    remarks = app_db.Column(app_db.Text, default='Без замечаний')
    event_description = app_db.Column(app_db.Text)

    def __repr__(self):
        return '<Switching report %r' % self.id

    def to_dict(self):
        return {
            'Creation date':self.creation_date,
            'Modified date':self.modified_date,
            'Satellite':self.satellite,
            'Polarization':f'U/L:{self.u_l_polarization}; D/L:{self.d_l_polarization}',
            'Frequency':f'U/L:{self.u_l_frequency}; D/L:{self.d_l_frequency};',
            'Signal description':self.signal_description,
            'Signal format':f'AR:{self.aspect_ratio}, PS:{self.production_standard}, DS:{self.distribution_standard}',
            'Modulation':self.modulation,
            'Encryption':f'{self.encryption_biss}, {self.encryption_code}',
            'Audion configuration':f'{self.audio_configuration}'
        }
