import pandas
from pandas import DataFrame
from datetime import datetime
from switching_reports.models.dataframe_handler import getMergeIndexesWithSameValue
from io import BytesIO


#GLOBALS
XLSX_CELL_FORMATS = {'date_format': {'align':'center', 'valign': 'vcenter', 'border': 1, 'num_format':'dd-mm-yyyy'},
                     'text_format': {'align':'center', 'valign': 'vcenter', 'border': 1},
                     'default_cell_format':{'align': 'center', 'valign': 'vcenter', 'border': 1}}
SHEET_NAME = 'Switching_reports'
XLSX_ENGINE = 'xlsxwriter'


def _addDateFormatToWorksheet(workbook, format_name='date_format'):
    return workbook.add_format(XLSX_CELL_FORMATS[format_name])

def _addTextFormatToWorksheet(workbook, format_name='text_format'):
    return workbook.add_format(XLSX_CELL_FORMATS[format_name])

def _mergeSimilarColumns(worksheet, merge_indexes, col_name, format):
    for indexes_tuple in merge_indexes:
        start_index, end_index, merge_data = indexes_tuple
        worksheet.merge_range(start_index, MERGE_COL_NUMBERS[col_name], end_index, MERGE_COL_NUMBERS[col_name], merge_data, format)

def _getXlsxFormats(workbook):
    return (_addDateFormatToWorksheet(workbook), _addTextFormatToWorksheet(workbook))

def _formatExcelData(writer:pandas.ExcelWriter, workbook):
    worksheet = writer.sheets[SHEET_NAME]

    default_format = workbook.add_format(XLSX_CELL_FORMATS['default_cell_format'])
    for col_excel_name in [chr(x) for x in range(65, 75)]:
        worksheet.set_column(f'{col_excel_name}:{col_excel_name}', 50, cell_format=default_format)

def _mergeCellsWithSameDate(dataframe:DataFrame, workbook, worksheet):
    date_format = _getXlsxFormats(workbook)[0]

    date_merge_indexes = getMergeIndexesWithSameValue(dataframe, list(MERGE_COL_NUMBERS.keys())[0])
    _mergeSimilarColumns(worksheet, date_merge_indexes, list(MERGE_COL_NUMBERS.keys())[0], date_format)

def _mergeCellsWithSameValues(dataframe:DataFrame, workbook, worksheet):
    text_format = _getXlsxFormats(workbook)[1]
    date_merge_indexes = getMergeIndexesWithSameValue(dataframe, list(MERGE_COL_NUMBERS.keys())[0])

    for date_merge_index_tuple in date_merge_indexes:
        merge_boundaries = date_merge_index_tuple[0], date_merge_index_tuple[1]
        for col_name in MERGE_COL_NUMBERS.keys():
            if not col_name == 'Дата создания':
                _mergeSimilarColumns(worksheet, getMergeIndexesWithSameValue(dataframe, col_name, merge_boundaries), col_name, text_format)

def getReadableFilenameFromDates(from_date:datetime, to_date:datetime):
    return f"{from_date.strftime('%Y-%m-%d')}_{to_date.strftime('%Y-%m-%d')}.xlsx"

def writeDataframeToXlsx(dataframe:DataFrame):
    output = BytesIO()
    writer = pandas.ExcelWriter(output, engine=XLSX_ENGINE)

    dataframe.to_excel(writer, index=False, startrow=0, sheet_name=SHEET_NAME)
    worksheet = writer.sheets[SHEET_NAME]
    workbook = writer.book

    _mergeCellsWithSameDate(workbook, worksheet)
    _mergeCellsWithSameValues(workbook, worksheet)

    writer.close()
    output.seek(0)

    return output




