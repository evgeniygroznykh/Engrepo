import pandas
from pandas import DataFrame


#GLOBALS
MERGE_COLUMNS = ['Дата создания', 'Заказчик', 'Исполнители']
COLUMN_NAMES_TO_FORMAT = ['Дата редактирования', 'Начало трансляции', 'Окончание трансляции']
CREATION_DATE_COLUMN_NAME = 'Дата создания'

def _formatDateToDayOnly(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.date


def _formatDateTo24H(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.strftime('%Y-%m-%d %H:%M')


def _sortDataframe(dataframe):
    dataframe.sort_values(by=MERGE_COLUMNS, ascending=[True, True, True],
                              inplace=True, ignore_index=True)


def getMergeBoundaryIndexes(dataframe, col_name='Дата создания'):
    merge_bound_indexes = []
    start_index = 1
    end_index = 1
    for row in range(0, len(dataframe[col_name])):
        if row == len(dataframe[col_name])-1:
            merge_bound_indexes.append((start_index, end_index, dataframe.loc[row, col_name]))
        else:
            if dataframe.loc[row, col_name] == dataframe.loc[row+1, col_name]:
                end_index += 1
            else:
                merge_bound_indexes.append((start_index, end_index, dataframe.loc[row, col_name]))
                start_index = end_index + 1
                end_index = start_index
    return merge_bound_indexes


def getLocalMergeIndexes(boundary_indexes, col_name, dataframe):
    local_merge_indexes = []
    left_bound, right_bound = boundary_indexes[0], boundary_indexes[1]

    start_index = left_bound
    end_index = start_index
    for row in range(left_bound-1, right_bound):
        if row == right_bound-1:
            local_merge_indexes.append((start_index, end_index, dataframe.loc[row, col_name]))
        else:
            if dataframe.loc[row, col_name] == dataframe.loc[row+1, col_name]:
                end_index += 1
            else:
                local_merge_indexes.append((start_index, end_index, dataframe.loc[row, col_name]))
                start_index = end_index + 1
                end_index = start_index
    return {col_name:local_merge_indexes}


def getDataframeFromSwitchingReports(sw_reports:list):
    return pandas.DataFrame.from_records([sw_report.to_dict() for sw_report in sw_reports])


def formatDataframeForXlsxUpload(raw_dataframe:DataFrame):
    _formatDateToDayOnly(raw_dataframe, CREATION_DATE_COLUMN_NAME)
    for col_name in COLUMN_NAMES_TO_FORMAT:
        _formatDateTo24H(raw_dataframe, col_name)
    _sortDataframe(raw_dataframe)
    formatted_dataframe = raw_dataframe
    return formatted_dataframe
