from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import log_db_connection_error_and_reraise
import os

class DatabaseContext:
    def setupApplicationDatabase(app:Flask, config):
        app.config['SQLALCHEMY_DATABASE_URI'] = config['database-uri']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def initializeDatabaseAndCreateTables(database, app:Flask):
        try:
            database.app = app
            database.init_app(app)
            database.create_all()
            return database
        except SQLAlchemyOperationalError as exc:
            log_db_connection_error_and_reraise(exc, 'Database is not available, check database connection.')



