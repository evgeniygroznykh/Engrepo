from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import logDBConnectionErrorAndReraise
from switching_reports.models.switching_report import SwitchingReport


class DatabaseContext:
    @staticmethod
    def setupApplicationDatabase(app:Flask, config):
        app.config['SQLALCHEMY_DATABASE_URI'] = config['database-uri']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @staticmethod
    def initializeDatabaseAndCreateTables(database, app:Flask):
        try:
            database.app = app
            database.init_app(app)
            database.create_all()
        except SQLAlchemyOperationalError as exc:
            logDBConnectionErrorAndReraise(exc, 'Database is not available, check database connection.')

    @staticmethod
    def addSwitchingReportToDatabase(database, switching_report:SwitchingReport):
        try:
            database.session.add(switching_report)
            database.session.commit()
        except Exception as exc:
            return 'Args: %s; Error: %s;' % (exc.args, exc)

    @staticmethod
    def deleteSwitchingReportFromDatabase(database, switching_report:SwitchingReport):
        try:
            database.session.delete(switching_report)
            database.session.commit()
        except:
            return "При удалении отчета произошла ошибка"