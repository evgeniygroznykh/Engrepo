from switching_reports.models.switching_report import SwitchingReport
from models.dbconn import DatabaseContext
from sqlalchemy import or_, and_


@DatabaseContext.databaseConnectionHandler
def getSwitchingReportsFromDatabaseUsingSearchString(search_string:str):
    needed_switching_reports = SwitchingReport.query.filter(or_(SwitchingReport.work_type.ilike(f'%{search_string}%'),
                                                                SwitchingReport.comment.ilike(f'%{search_string}%'),
                                                                SwitchingReport.shift_comp.ilike(f'%{search_string}%'))) \
        .order_by(SwitchingReport.date.desc()).all()
    return needed_switching_reports

@DatabaseContext.databaseConnectionHandler
def getSwitchingReportsFromDatabaseUsingDateFilter(filter_from_date, filter_to_date):
    filtered_switching_reports = SwitchingReport.query.filter(
        and_(SwitchingReport.date >= filter_from_date, SwitchingReport.date <= filter_to_date)) \
        .order_by(SwitchingReport.date.desc()).all()
    return filtered_switching_reports