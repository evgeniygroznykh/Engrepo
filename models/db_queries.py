from models.database_context import databaseConnectionHandler
from sqlalchemy import or_, and_


#TODO: this module is not used for now due to the fact, that it doesn't get context of database model, so all queries return None
@databaseConnectionHandler
def getSwitchingReportsFromDatabaseUsingSearchString(database_model, search_string:str):
    needed_switching_reports = database_model.query.filter(or_(database_model.work_type.ilike(f'%{search_string}%'),
                                                                database_model.comment.ilike(f'%{search_string}%'),
                                                                database_model.shift_comp.ilike(f'%{search_string}%'))) \
        .order_by(database_model.date.desc()).all()
    print(database_model)
    print(needed_switching_reports)
    return needed_switching_reports

@databaseConnectionHandler
def getSwitchingReportsFromDatabaseUsingDateFilter(database_model, filter_from_date, filter_to_date):
    filtered_switching_reports = database_model.query.filter(
        and_(database_model.date >= filter_from_date, database_model.date <= filter_to_date)) \
        .order_by(database_model.date.desc()).all()
    return filtered_switching_reports
