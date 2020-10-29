import pandas
import xlsxwriter as xls
from datetime import datetime
from pandas import DataFrame
from io import BytesIO


#GLOBALS
XLSX_CELL_FORMATS = {'date_format': {'align':'center', 'valign': 'vcenter', 'border': 1, 'num_format':'dd-mm-yyyy'},
                     'text_format': {'align':'center', 'valign': 'vcenter', 'border': 1},
                     'default_cell_format':{'align': 'center', 'valign': 'vcenter', 'border': 1}}
MERGE_COL_NUMBERS = {'Дата создания': 0, 'Заказчик': 8, 'Исполнители': 9}
SHEET_NAME = 'Switching_reports'
XLSX_ENGINE = 'xlsxwriter'


def getReadableFilenameFromDates(from_date:datetime, to_date:datetime):
    return f"{from_date.strftime('%Y-%m-%d')}_{to_date.strftime('%Y-%m-%d')}.xlsx"

def getDataframeFromSwitchingReports(sw_reports:list):
    return pandas.DataFrame.from_records([sw_report.to_dict() for sw_report in sw_reports])

def getMergeIndexes(df:DataFrame, col_name):
    merge_indexes = []
    start_index = 1
    end_index = 1
    for row in range(0, len(df[col_name])):
        if row == len(df[col_name])-1:
            merge_indexes.append((start_index, end_index, df.loc[row, col_name]))
        else:
            if df.loc[row, col_name] == df.loc[row+1, col_name]:
                end_index += 1
            else:
                merge_indexes.append((start_index, end_index, df.loc[row, col_name]))
                start_index = end_index + 1
                end_index = start_index
    return merge_indexes

def addDateFormatToWorksheet(workbook, format_name='date_format'):
    return workbook.add_format(XLSX_CELL_FORMATS[format_name])

def addTextFormatToWorksheet(workbook, format_name='text_format'):
    return workbook.add_format(XLSX_CELL_FORMATS[format_name])

def mergeSimilarColumns(worksheet, merge_indexes, col_name, format):
    for indexes_tuple in merge_indexes:
        start_index, end_index, merge_data = indexes_tuple
        worksheet.merge_range(start_index, MERGE_COL_NUMBERS[col_name], end_index, MERGE_COL_NUMBERS[col_name], merge_data, format)

def formatDateToDayOnly(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.date

def formatDateWithoutAMPM(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.strftime('%Y-%m-%d %H:%M')

def writeDataframeToXlsx(dataframe:DataFrame):
    output = BytesIO()
    writer = pandas.ExcelWriter(output, engine=XLSX_ENGINE)

    #Get date only
    formatDateToDayOnly(dataframe, list(MERGE_COL_NUMBERS.keys())[0])

    #Format translation times
    formatDateWithoutAMPM(dataframe, 'Дата редактирования')
    formatDateWithoutAMPM(dataframe, 'Начало трансляции')
    formatDateWithoutAMPM(dataframe, 'Окончание трансляции')

    dataframe.to_excel(writer, index=False, startrow=0, sheet_name=SHEET_NAME)

    workbook = writer.book
    worksheet = writer.sheets[SHEET_NAME]

    #Format all data in excel
    default_format = workbook.add_format(XLSX_CELL_FORMATS['default_cell_format'])
    for col_excel_name in [chr(x) for x in range(65, 75)]:
        worksheet.set_column(f'{col_excel_name}:{col_excel_name}', 50, cell_format=default_format)

    #Merge same data
    date_format = addDateFormatToWorksheet(workbook)
    text_format = addTextFormatToWorksheet(workbook)
    for col_name in MERGE_COL_NUMBERS.keys():
        mergeSimilarColumns(worksheet, getMergeIndexes(dataframe, col_name), col_name, date_format if col_name == 'Дата создания' else text_format)

    writer.close()
    output.seek(0)

    return output




