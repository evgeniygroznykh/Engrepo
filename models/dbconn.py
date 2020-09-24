from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import logDBConnectionErrorAndReraise


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
            return database
        except SQLAlchemyOperationalError as exc:
            logDBConnectionErrorAndReraise(exc, 'Database is not available, check database connection.')
