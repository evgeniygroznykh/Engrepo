import os
from switching_reports.models.switching_report_request_file import SwitchingReportRequestFile


class FileHandler:
    @staticmethod
    def isFileInRequestForm(request_file:SwitchingReportRequestFile):
        return request_file.request_file_instance.filename == ''

    @staticmethod
    def isRequestFileExists(request_file:SwitchingReportRequestFile):
        return os.path.isfile(request_file.request_file_path)

    @staticmethod
    def uploadRequestFile(request_file:SwitchingReportRequestFile):
        request_file.request_file_instance.save(request_file.request_file_path)


