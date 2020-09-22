from flask import Flask
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from models.logger import log_db_connection_error_and_reraise
import os

class DBContext():
    @staticmethod
    def setup_db(app:Flask):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EngrepoDB'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @staticmethod
    def create_db(database, app:Flask):
        try:
            database.app = app
            database.init_app(app)
            database.create_all()
            return database
        except SQLAlchemyOperationalError as exc:
            log_db_connection_error_and_reraise(exc, 'Database is not available, check database connection.')


    @staticmethod
    def verify_db(db_name):
        def func_decorator(func):
            def wrapper():
                if not os.path.exists(os.path.join(os.getcwd(), db_name)):
                    func()
            return wrapper
        return func_decorator


