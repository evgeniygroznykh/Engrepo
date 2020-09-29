import os
import traceback
from datetime import datetime as dt


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
@logFileUnavailableHandler("Log file is unavailable. Please check permissions and that log file exists and it has correct format.")
def handleGeneralExceptions(exc:Exception, message:str):
	with open('logs/app_log.txt', 'a+', encoding='utf-8') as log_file:
		if exc is FileNotFoundError:
			print(f"{dt.now()} | {message} | {exc.strerror} => {exc.filename}", file=log_file)
		elif exc is OSError:
			print(f"{dt.now()} | {message} | {exc.strerror}", file=log_file)
		else:
			print(f"{dt.now()} | {message} | {exc.args}", file=log_file)
