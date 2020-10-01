from models.shared_db import application_database as app_db
from switching_reports.models.switching_report_request_file import SwitchingReportRequestFile
from switching_reports.models.switching_report_service_data import SwitchingReportServiceData
from switching_reports.models.switching import Switching
from switching_reports.models.translation import Translation
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
    reserve_source = app_db.Column(app_db.String(50))
    main_destination = app_db.Column(app_db.String(50), nullable=False)
    reserve_destination = app_db.Column(app_db.String(50))
    customer = app_db.Column(app_db.String(50), nullable=False)
    remarks = app_db.Column(app_db.Text, default='Без замечаний')
    request_file_path = app_db.Column(app_db.Text)

    def __repr__(self):
        return '<Switching report %r' % self.id

    def to_dict(self):
        return {
            'Дата':self.date,
            'Комментарий':self.comment,
            'Виды работ':self.work_type,
            'Начало трансляции':self.translation_start_time,
            'Окончание трансляции':self.translation_end_time,
            'Источник':f'{self.main_source} {self.reserve_source}',
            'Направление':f'{self.main_destination} {self.reserve_destination}',
            'Заказчик':self.customer,
            'Исполнители':self.shift_comp
        }

    def updateRequestFilePath(self, switching_report_request_file:SwitchingReportRequestFile):
        if self.request_file_path == 'no request file':
            self.request_file_path = self.request_file_path. \
                replace('no request file', switching_report_request_file.request_file_path)
        else:
            self.request_file_path += f'; {switching_report_request_file.request_file_path}'

    def updateServiceData(self, new_service_data:SwitchingReportServiceData):
        self.date = new_service_data.date
        self.work_type = new_service_data.work_type
        self.customer = new_service_data.customer
        self.shift_comp = new_service_data.shift_composition
        self.comment = new_service_data.comment
        self.remark = new_service_data.remarks

    def updateTranslationData(self, new_translation_data:Translation):
        self.translation_start_time = new_translation_data.stringifyStartTime()
        self.translation_end_time = new_translation_data.stringifyEndTime()

    def updateSwitchingData(self, new_switching_data:Switching):
        self.main_source = new_switching_data.main_source
        self.main_destination = new_switching_data.main_destination
        self.reserve_source = new_switching_data.reserve_source
        self.reserve_destination = new_switching_data.reserve_destination

    def formatTranslationStartTimeForJinja(self):
        return dt.strftime(self.translation_start_time, '%Y-%m-%dT%H:%M')

    def formatTranslationEndTimeForJinja(self):
        return dt.strftime(self.translation_end_time, '%Y-%m-%dT%H:%M')

    def formatRemarksOnRequestFileExistsErrorFix(self, error_template:str):
        if error_template in self.remarks:
            self.remarks = self.remarks.replace(error_template, '')

    def formatRemarksIfNoRemarks(self):
        if self.remarks == '':
            self.remarks = 'Без замечаний'

    def formatRemarksOnReportUpdate(self, error_template:str):
        self.remarks = error_template if self.remarks == 'Без замечаний' else self.remarks + f'; {error_template}'

    @staticmethod
    def formatRemarksOnReportCreation(remarks:str, error_template:str):
        remarks = error_template if remarks == 'Без замечаний' else remarks + f'; {error_template}'

    @staticmethod
    def getReportingPeriodAsTuple(period_in_days:int):
        now = dt.now()
        default_to_value = now.__format__("%Y-%m-%dT%H:%M")
        default_from_value = (now-timedelta(days=period_in_days)).__format__("%Y-%m-%dT%H:%M")
        return (default_from_value, default_to_value)

    @staticmethod
    def getTimeDeltas(period_in_days:int):
        return [timedelta(days=i) for i in range(period_in_days)]
