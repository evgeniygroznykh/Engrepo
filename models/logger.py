import os
from datetime import datetime as dt
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError


def createLogFilesDirIfNotExists(logged_func):
	def wrapper():
		try:
			if not os.path.exists('logs'):
				os.mkdir('logs')
			logged_func()
			return wrapper
		except OSError as exc:
			print(f'An error occured on operation system level. {exc.strerror}')

@createLogFilesDirIfNotExists
def logFileNotFoundErrorAndReraise(exc:FileNotFoundError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.strerror} => {exc.filename}", file=log_file)
	raise

@createLogFilesDirIfNotExists
def logDBConnectionErrorAndReraise(exc:SQLAlchemyOperationalError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.args}", file=log_file)
	raise

@createLogFilesDirIfNotExists
def logOSErrorAndReraise(exc:OSError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.strerror}", file=log_file)
	raise