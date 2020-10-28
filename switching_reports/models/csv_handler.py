import pandas
from datetime import datetime
from pandas import DataFrame
from io import BytesIO


def getReadableFilenameFromDates(from_date:datetime, to_date:datetime):
    return f"{from_date.strftime('%Y-%m-%d')}_{to_date.strftime('%Y-%m-%d')}.xlsx"

def getDataframeFromSwitchingReports(sw_reports:list):
    return pandas.DataFrame.from_records([sw_report.to_dict() for sw_report in sw_reports])

def writeDataframeToXlsx(dataframe:DataFrame):
    output = BytesIO()

    writer = pandas.ExcelWriter(output, engine='xlsxwriter')

    dataframe['Дата создания'] = pandas.to_datetime(dataframe['Дата создания'])
    dataframe.to_excel(writer, index=False, startrow=0, sheet_name='Switching_reports')
    worksheet = writer.sheets["Switching_reports"]
    worksheet.set_column(0, 9, 28)

    writer.close()
    output.seek(0)

    return output



