import pandas
from pandas import DataFrame


#GLOBALS
COLUMN_NAMES_TO_FORMAT = ['Дата редактирования', 'Начало трансляции', 'Окончание трансляции']
MERGE_COL_NUMBERS = {'Дата создания': 0, 'Заказчик': 8, 'Исполнители': 9}

def _formatDateToDayOnly(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.date

def _formatDateTo24H(dataframe, col_name):
    dataframe[col_name] = pandas.to_datetime(dataframe[col_name]).dt.strftime('%Y-%m-%d %H:%M')

def getMergeIndexesWithSameValue(df:DataFrame, col_name, index_boundaries=None):
    merge_indexes = []
    if index_boundaries:
        left_bound, right_bound = index_boundaries
        start_index = left_bound
        end_index = start_index
        for row in range(left_bound-1, right_bound):
            if row == right_bound-1:
                merge_indexes.append((start_index, end_index, df.loc[row, col_name]))
            else:
                if df.loc[row, col_name] == df.loc[row+1, col_name]:
                    end_index += 1
                else:
                    merge_indexes.append((start_index, end_index, df.loc[row, col_name]))
                    start_index = end_index + 1
                    end_index = start_index
    else:
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

def getDataframeFromSwitchingReports(sw_reports:list):
    return pandas.DataFrame.from_records([sw_report.to_dict() for sw_report in sw_reports])

def formatDataframeForXlsxUpload(raw_dataframe:DataFrame):
    _formatDateToDayOnly(raw_dataframe, list(MERGE_COL_NUMBERS.keys())[0])
    _formatDateTo24H(raw_dataframe, 'Дата редактирования')
    _formatDateTo24H(raw_dataframe, 'Начало трансляции')
    _formatDateTo24H(raw_dataframe, 'Окончание трансляции')
    formatted_dataframe = raw_dataframe
    return formatted_dataframe
