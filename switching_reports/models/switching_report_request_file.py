from dataclasses import dataclass
from werkzeug.datastructures import FileStorage

@dataclass
class SwitchingReportRequestFile:
    request_file_instance : FileStorage
    request_file_path : str