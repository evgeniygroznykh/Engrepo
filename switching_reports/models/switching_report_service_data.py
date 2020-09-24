from dataclasses import dataclass
from datetime import datetime


@dataclass
class SwitchingReportServiceData:
    date : datetime
    work_type : str
    customer : str
    shift_composition : str
    comment : str
    remarks : str