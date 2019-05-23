from flask import Config
import sys

class Path():

	def __init__(self, name = 'production'):
		PROD = 'production'
		MAX = 'max'
		MATT = 'matt'
		if (name == MATT):
			self.absolute_path = '/Users/matveyturkov/Python_Project'
		if (name == MAX):
			self.absolute_path = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project'
		if (name == PROD):
			self.absolute_path = '/home/ubuntu/Python_Project'

	def personal_info(self):
		return (self.absolute_path + '/personal_info')

	def markov_chain(self):
		return (self.absolute_path + '/analysis/markovs_chain/Python')


paths = Path('production')
sys.path.insert(0, paths.personal_info())
from personal_constants import *

class DevelopmentMaxConfig(Config):
	DB = DB_maxim
	USER = USER_maxim
	PASSWORD = PASSWORD_maxim
	HOST = HOST_maxim
	PORT = PORT_maxim
	SQL_PATH = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/sql/'
	SCRIPTS_PATH = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/scripts/'
	CLIENT_CLASS = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/server_data_tmp/app'

class DevelopmentMatveyConfig(Config):
	DB = DB_matvey
	USER = USER_matvey
	PASSWORD = PASSWORD_matvey
	HOST = HOST_matvey
	PORT = PORT_matvey
	SQL_PATH = '/Users/matveyturkov/Python_Project/sql'
	SCRIPTS_PATH = '/Users/matveyturkov/Python_Project/scripts/'
	CLIENT_CLASS = '/Users/matveyturkov/Python_Project/server_data_tmp/app/'


class ProductionConfig(Config):
	DB = DB_server
	USER = USER_server
	PASSWORD = PASSWORD_server
	HOST = HOST_server
	PORT = None
	SQL_PATH = '/home/ubuntu/Python_Project/sql'
	SCRIPTS_PATH = '/home/ubuntu/Python_Project/scripts/'
	CLIENT_CLASS = '/home/ubuntu/Python_Project/server_data_tmp/app/'







