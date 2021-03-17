from dataclasses import dataclass
from datetime import datetime


@dataclass
class SwitchingReportServiceData:
    creation_date : datetime
    modified_date : datetime
    report_header : str
    work_type : str
    customer : str
    shift_composition : str
    comment : str
    remarks : str
