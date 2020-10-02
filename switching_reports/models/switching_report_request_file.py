from dataclasses import dataclass
from werkzeug.datastructures import FileStorage

@dataclass
class SwitchingReportRequestFile:
    request_file_instance:FileStorage
    request_file_path:str = 'no request file'

    def setFilePath(self, update_folder:str):
        self.request_file_path = update_folder + self.request_file_instance.filename

