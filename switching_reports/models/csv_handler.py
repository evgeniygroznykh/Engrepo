import pandas
from datetime import datetime
from pandas import DataFrame


def getReadableFilenameFromDates(from_date:datetime, to_date:datetime):
    return f"{from_date.strftime('%Y-%m-%d')}_{to_date.strftime('%Y-%m-%d')}.csv"

def getDataframeFromSwitchingReports(sw_reports:list):
    return pandas.DataFrame.from_records([sw_report.to_dict() for sw_report in sw_reports])

def writeDataframeToCsv(dataframe:DataFrame):
    return dataframe.to_csv(index=False, encoding='utf-16', sep=',')


