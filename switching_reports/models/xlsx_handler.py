import pandas
from pandas import DataFrame
from datetime import datetime
from io import BytesIO
from switching_reports.models.dataframe_handler import getMergeBoundaryIndexes, getLocalMergeIndexes


#GLOBALS
XLSX_CELL_FORMATS = {'short_date_time_format': {'align':'center', 'valign': 'vcenter', 'border': 1, 'num_format':'yyyy-mm-dd'},
                    'full_date_time_format': {'align':'center', 'valign': 'vcenter', 'border': 1, 'num_format':'yyyy-mm-dd HH-MM'},
                     'text_format': {'align':'center', 'valign': 'vcenter', 'border': 1},
                     'default_cell_format':{'align': 'center', 'valign': 'vcenter'}}
SHEET_NAME = 'Switching_reports'
XLSX_ENGINE = 'xlsxwriter'
MERGE_COLUMNS = ['Дата создания', 'Заказчик', 'Исполнители']
MERGE_COL_NUMBERS = {'Дата создания': 0, 'Исполнители': 9, 'Заказчик': 8}
SHORT_DATETIME_COLUMNS = ['Дата создания']
FULL_DATETIME_COLUMNS = ['Дата редактирования', 'Начало трансляции', 'Окончание трансляции']
COLOR_FLAG = True


def _getCellFormat(col_name, workbook):
    if col_name in SHORT_DATETIME_COLUMNS:
        format_name = 'short_date_time_format'
        XLSX_CELL_FORMATS[format_name]['bg_color'] = 'gray' if COLOR_FLAG else 'white'
    elif col_name in FULL_DATETIME_COLUMNS:
        format_name = 'full_date_time_format'
        XLSX_CELL_FORMATS[format_name]['bg_color'] = 'gray' if COLOR_FLAG else 'white'
    else:
        format_name = 'text_format'
        XLSX_CELL_FORMATS[format_name]['bg_color'] = 'gray' if COLOR_FLAG else 'white'
    return workbook.add_format(XLSX_CELL_FORMATS[format_name])


def _formatColumns(writer):
    worksheet = writer.sheets[SHEET_NAME]
    workbook = writer.book

    default_format = workbook.add_format(XLSX_CELL_FORMATS['default_cell_format'])
    for col_excel_name in [chr(x) for x in range(65, 75)]:
        print(f'Setting format for column {col_excel_name}:{col_excel_name}')
        worksheet.set_column(f'{col_excel_name}:{col_excel_name}', 50, cell_format=default_format)


def _fillRows(writer, date_boundary_indexes):
    global COLOR_FLAG
    workbook = writer.book
    worksheet = writer.sheets[SHEET_NAME]

    bg_color = 'gray' if COLOR_FLAG else 'white'
    lower_bound, upper_bound = date_boundary_indexes[0], date_boundary_indexes[1]

    bg_color_cell_format = workbook.add_format({'align':'center', 'valign':'center', 'bg_color':bg_color, 'border':1})
    for row in range(lower_bound, upper_bound+1):
        worksheet.set_row(row, None, bg_color_cell_format)
    COLOR_FLAG = False if COLOR_FLAG else True


def _mergeRows(local_merge_indexes, col_name, writer):
    column_number = MERGE_COL_NUMBERS[col_name]
    for cur_merge_data in local_merge_indexes[col_name]:
        start_merge_idx, end_merge_idx, merge_val = cur_merge_data
        workbook = writer.book
        worksheet = writer.sheets[SHEET_NAME]

        merge_format = _getCellFormat(col_name, workbook)
        worksheet.merge_range(start_merge_idx, column_number, end_merge_idx, column_number, merge_val, merge_format)


def getReadableFilenameFromDates(from_date:datetime, to_date:datetime):
    return f"{from_date.strftime('%Y-%m-%d')}_{to_date.strftime('%Y-%m-%d')}.xlsx"


def writeDataframeToXlsx(dataframe:DataFrame):
    merge_boundary_indexes_from_date = getMergeBoundaryIndexes(dataframe)

    output = BytesIO()
    writer = pandas.ExcelWriter(output, engine=XLSX_ENGINE)

    dataframe.to_excel(writer, index=False, startrow=0, sheet_name=SHEET_NAME)
    _formatColumns(writer)

    for cur_merge_boundaries in merge_boundary_indexes_from_date:
        for col in MERGE_COLUMNS:
            col_local_merge_indexes = getLocalMergeIndexes(cur_merge_boundaries, col, dataframe)
            _mergeRows(col_local_merge_indexes, col, writer)
        _fillRows(writer, cur_merge_boundaries)

    writer.close()
    output.seek(0)

    return output
