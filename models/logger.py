import os
import traceback
from datetime import datetime as dt
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError


def createLogFilesDirIfNotExists(logged_func):
	def wrapper(*args, **kwargs):
		try:
			if not os.path.exists('logs'):
				os.mkdir('logs')
			logged_func(*args, **kwargs)
			return wrapper
		except OSError as exc:
			print(f'An error occured on operation system level. {exc.strerror}')
	return wrapper

def logFileUnavailableHandler(error_message):
	def wrapper(func):
		def printErrorMessage(*args):
			try:
				func(*args)
			except:
				print(error_message)
		return printErrorMessage
	return wrapper

@createLogFilesDirIfNotExists
@logFileUnavailableHandler("Log file is unavailable. An occured 'file not found' error wasn't logged.")
def logFileNotFoundErrorAndReraise(exc:FileNotFoundError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.strerror} => {exc.filename}", file=log_file)

@createLogFilesDirIfNotExists
@logFileUnavailableHandler("Log file is unavailable. An occured 'database connection' error wasn't logged.")
def logDBConnectionErrorAndReraise(exc:SQLAlchemyOperationalError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.args}", file=log_file)

@createLogFilesDirIfNotExists
@logFileUnavailableHandler("Log file is unavailable. An occured 'operating system' error wasn't logged.")
def logOSErrorAndReraise(exc:OSError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.strerror}", file=log_file)

@createLogFilesDirIfNotExists
@logFileUnavailableHandler("Log file is unavailable. An occured 'attribute' error wasn't logged.")
def logAttributeErrorAndReraise(exc:AttributeError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.args}", file=log_file)
		print(traceback.print_exc(), file=log_file)

@createLogFilesDirIfNotExists
@logFileUnavailableHandler
def logKeyErrorAndReraise(exc:KeyError, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		print(f"{dt.now()} | {message} | {exc.args}", file=log_file)