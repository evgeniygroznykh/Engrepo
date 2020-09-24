from dataclasses import dataclass
from datetime import datetime


@dataclass
class Translation:
    start_time : datetime
    end_time : datetime

    def stringifyStartTime(self):
        return datetime.strftime(self.start_time, '%Y-%m-%dT%H:%M')

    def stringifyEndTime(self):
        return datetime.strftime(self.end_time, '%Y-%m-%dT%H:%M')

    def getTranslationDuration(self):
        return self.end_time - self.start_time