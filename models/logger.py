from datetime import datetime as dt
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError


def log_file_not_found_and_reraise(exc:FileNotFoundError, message:str):
    with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
        print(f"{dt.now()} | {message} | {exc.strerror} => {exc.filename}", file=log_file)
    raise

def log_db_connection_error_and_reraise(exc:SQLAlchemyOperationalError, message:str):
    with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
        print(f"{dt.now()} | {message} | {exc.args}", file=log_file)
    raise