from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import handleGeneralExceptions
from switching_reports.models.switching_report import SwitchingReport
from teleport.models.teleport_record import TeleportRecord


#GLOBALS
CONFIG_DATABASE_URI_KEY = 'database-uri'
#ENDGLOBALS

def databaseConnectionHandler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SQLAlchemyOperationalError as exc:
            handleGeneralExceptions(exc, 'Database is not available, check database connection.')
    return wrapper

def databaseSessionCommitChanges(database):
    database.session.commit()

class DatabaseContext:
    @staticmethod
    def setupApplicationDatabase(app:Flask, config):
        app.config['SQLALCHEMY_DATABASE_URI'] = config[CONFIG_DATABASE_URI_KEY]
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @staticmethod
    @databaseConnectionHandler
    def initializeDatabaseAndCreateTables(database, app:Flask):
        database.app = app
        database.init_app(app)
        database.create_all()

    @staticmethod
    @databaseConnectionHandler
    def databaseSessionCommitChanges(database):
        database.session.commit()

    @staticmethod
    @databaseConnectionHandler
    def addSwitchingReportToDatabase(database, switching_report:SwitchingReport):
        database.session.add(switching_report)
        databaseSessionCommitChanges(database)

    @staticmethod
    @databaseConnectionHandler
    def addTeleportRecordToDatabase(database, teleport_record:TeleportRecord):
        database.session.add(teleport_record)
        databaseSessionCommitChanges(database)

    @staticmethod
    @databaseConnectionHandler
    def deleteSwitchingReportFromDatabase(database, switching_report:SwitchingReport):
        database.session.delete(switching_report)
        databaseSessionCommitChanges(database)