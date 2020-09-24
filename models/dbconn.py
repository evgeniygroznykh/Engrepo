from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import logDBConnectionErrorAndReraise
from switching_reports.models.switching_report import SwitchingReport


class DatabaseContext:
    @staticmethod
    def databaseConnectionHandler(func):
        def wrapper():
            try:
                func()
            except SQLAlchemyOperationalError as exc:
                logDBConnectionErrorAndReraise(exc, 'Database is not available, check database connection.')
        return wrapper

    @staticmethod
    def setupApplicationDatabase(app:Flask, config):
        app.config['SQLALCHEMY_DATABASE_URI'] = config['database-uri']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @staticmethod
    @databaseConnectionHandler
    def initializeDatabaseAndCreateTables(database, app:Flask):
        database.app = app
        database.init_app(app)
        database.create_all()

    @staticmethod
    @databaseConnectionHandler
    def addSwitchingReportToDatabase(database, switching_report:SwitchingReport):
        database.session.add(switching_report)
        database.session.commit()

    @staticmethod
    @databaseConnectionHandler
    def deleteSwitchingReportFromDatabase(database, switching_report:SwitchingReport):
        database.session.delete(switching_report)
        database.session.commit()

    @staticmethod
    @databaseConnectionHandler
    def databaseSessionCommitChanges(database):
        database.session.commit()
