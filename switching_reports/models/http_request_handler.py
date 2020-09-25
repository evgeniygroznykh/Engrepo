from flask import request
from datetime import datetime as dt
from switching_reports.models.switching import Switching
from switching_reports.models.translation import Translation
from switching_reports.models.switching_report_request_file import SwitchingReportRequestFile
from switching_reports.models.switching_report_service_data import SwitchingReportServiceData
from models.logger import logKeyError, logValueError


class HttpRequestHandler:
    @staticmethod
    def getTranslationInstanceFromReqForm():
        try:
            start_time = dt.strptime(request.form['translationStartTime'], '%Y-%m-%dT%H:%M')
            end_time = dt.strptime(request.form['translationEndTime'], '%Y-%m-%dT%H:%M')
            translation = Translation(start_time, end_time)
            return translation
        except KeyError as exc:
            logKeyError(exc, "Some of the translation data keys weren't found in request form.")

    @staticmethod
    def getSwitchingInstanceFromReqForm():
        try:
            switching_source = request.form['switchingSource']
            switching_destination = request.form['switchingDestination']
            switching_reserve_source = request.form['reserveSwitchingSource']
            switching_reserve_destination = request.form['reserveSwitchingDestination']
            switching = Switching(switching_source, switching_destination, switching_reserve_source, switching_reserve_destination)
            return switching
        except KeyError as exc:
            logKeyError(exc, "Some of the switching data keys weren't found in request form.")


    @staticmethod
    def getRequestFileInstanceFromReqForm():
        try:
            request_file_from_form = request.files['requestFile']
            return SwitchingReportRequestFile(request_file_from_form)
        except KeyError as exc:
            logKeyError(exc, "'requestFile' wasn't found in request form.")

    @staticmethod
    def getSwitchingReportServiceDataFromReqForm():
        try:
            date = dt.now()
            work_type = request.form['switchingReportWorkType']
            customer = request.form['switchingCustomer']
            shift_composition = request.form['shiftComp']
            comment = request.form['switchingReportComment']
            remarks = request.form['switchingReportRemarks']
            service_data = SwitchingReportServiceData(date, work_type, customer, shift_composition, comment, remarks)
            return service_data
        except KeyError as exc:
            logKeyError(exc, "Some of the service data keys weren't found in request form.")

    @staticmethod
    def getReportingPeriodFromFilterForm():
        try:
            filter_from_date = dt.strptime(request.form['sortStartTime'], '%Y-%m-%dT%H:%M')
            filter_to_date = dt.strptime(request.form['sortEndTime'], '%Y-%m-%dT%H:%M')
            days = (filter_to_date - filter_from_date).days
            return (filter_from_date, filter_to_date, days)
        except KeyError as key_exc:
            logKeyError(key_exc, "'sortStartTime' or 'sortEndTime' wasn't found in request form.")
        except ValueError as val_exc:
            logValueError(val_exc, "'sortStartTime' or 'sortEndTime' have incorrect format.")

    @staticmethod
    def getSearchStringFromSearchForm():
        try:
            return request.form['search_string']
        except KeyError as exc:
            logKeyError(exc, "'search_string' wasn't found in request form.")


