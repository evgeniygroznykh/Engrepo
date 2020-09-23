from dataclasses import dataclass
from datetime import datetime


@dataclass
class Translation:
    start_time : datetime
    end_time : datetime

    def stringify_start_time(self):
        return datetime.strftime(self.start_time, '%Y-%m-%dT%H:%M')

    def stringify_end_time(self):
        return datetime.strftime(self.end_time, '%Y-%m-%dT%H:%M')

    def translation_duration(self):
        return self.end_time - self.start_time