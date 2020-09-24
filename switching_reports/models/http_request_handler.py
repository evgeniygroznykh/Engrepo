from flask import request
from datetime import datetime as dt
from switching_reports.models.switching import Switching
from switching_reports.models.translation import Translation
from switching_reports.models.switching_report_request_file import SwitchingReportRequestFile
from switching_reports.models.switching_report_service_data import SwitchingReportServiceData


class HttpRequestHandler:
    @staticmethod
    def getTranslationInstanceFromReqForm():
        start_time = dt.strptime(request.form['translationStartTime'], '%Y-%m-%dT%H:%M')
        end_time = dt.strptime(request.form['translationEndTime'], '%Y-%m-%dT%H:%M')
        translation = Translation(start_time, end_time)
        return translation

    @staticmethod
    def getSwitchingInstanceFromReqForm():
        switching_source = request.form['switchingSource']
        switching_destination = request.form['switchingDestination']
        switching_reserve_source = request.form['reserveSwitchingSource']
        switching_reserve_destination = request.form['reserveSwitchingDestination']
        switching = Switching(switching_source, switching_destination, switching_reserve_source, switching_reserve_destination)
        return switching

    @staticmethod
    def getRequestFileInstanceFromReqForm():
        request_file_from_form = request.files['requestFile']
        return SwitchingReportRequestFile(request_file_from_form)

    @staticmethod
    def getSwitchingReportServiceDataFromReqForm():
        date = dt.now()
        work_type = request.form['switchingReportWorkType']
        customer = request.form['switchingCustomer']
        shift_composition = request.form['shiftComp']
        comment = request.form['switchingReportComment']
        remarks = request.form['switchingReportRemarks']
        service_data = SwitchingReportServiceData(date, work_type, customer, shift_composition, comment, remarks)
        return service_data
