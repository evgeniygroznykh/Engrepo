import os
from switching_reports.models.switching_report_request_file import SwitchingReportRequestFile
from models.logger import handleGeneralExceptions


class FileHandler:
    @staticmethod
    def isFileInRequestForm(request_file:SwitchingReportRequestFile):
        try:
            return request_file.request_file_instance.filename == ''
        except AttributeError as exc:
            handleGeneralExceptions(exc, "Request file was NoneType, while trying to get it from request form.")

    @staticmethod
    def isRequestFileExistsInUploadFolder(upload_folder:str, request_file:SwitchingReportRequestFile):
        return os.path.isfile(os.path.join(upload_folder, request_file.request_file_instance.filename))

    @staticmethod
    def uploadRequestFile(upload_folder, request_file:SwitchingReportRequestFile):
        try:
            request_file.request_file_instance.save(os.path.join(os.getcwd(), upload_folder, request_file.request_file_instance.filename))
        except Exception as exc:
            handleGeneralExceptions(exc, "'Request file for this switching report was set, but not physically saved' error occured.")
