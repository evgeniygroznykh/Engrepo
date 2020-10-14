from dataclasses import dataclass
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


@dataclass
class SwitchingReportRequestFile:
    request_file_instance:FileStorage
    request_file_path:str = 'no request file'

    def setFilePath(self, update_folder:str):
        self.request_file_path = rf'{update_folder}/' + secure_filename(self.request_file_instance.filename)
