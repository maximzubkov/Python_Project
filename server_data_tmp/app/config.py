from flask import Config

class DevelopmentMaxConfig(Config):
	DB = 'zumamotu'
	USER = 'MaximZubkov'
	PASSWORD='maxTBMzu'
	HOST= "localhost"
	PORT='1234'
	SQL_PATH = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/sql/'
	SCRIPTS_PATH = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/scripts/'
	HISTORY_PATH = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/data/maxim_history.csv'
	CLIENT_CLASS = '/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/server_data_tmp/app'

class DevelopmentMatveyConfig(Config):
	DB = 'quack'
	USER = 'quack'
	PASSWORD=''
	HOST= "localhost"
	PORT='5432'
	SQL_PATH = '/Users/matveyturkov/Python_Project/sql'
	SCRIPTS_PATH = '/Users/matveyturkov/Python_Project/scripts/'
	HISTORY_PATH = '../../analysis/data/matvei_history.csv'
	CLIENT_CLASS = '/Users/matveyturkov/Python_Project/server_data_tmp/app/'


class ProductionConfig(Config):
	DB = 'zamamotu'
	USER = 'admin'
	PASSWORD = 'AhOJxy0uDf1T'
	HOST = "89.208.84.245"
	PORT = None
	SQL_PATH = '/Users/matveyturkov/Python_Project/sql'

