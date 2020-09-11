from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

class DBContext():
    @staticmethod
    def setup_db(app:Flask):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EngrepoDB'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @staticmethod
    def create_db(app:Flask):
        database = SQLAlchemy()
        database.app = app
        database.init_app(app)
        database.create_all()
        return database

    @staticmethod
    def verify_db(db_name):
        def func_decorator(func):
            def wrapper():
                if not os.path.exists(os.path.join(os.getcwd(), db_name)):
                    func()
            return wrapper
        return func_decorator


