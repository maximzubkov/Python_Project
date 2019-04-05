import psycopg2
class Sql():
	def __init__(self, db, user, password,host,port):
		self.db = db
		self.user = user
		self.password = password
		self.host = host
		self.port = port

	def get_connection(self):
		self.connect = psycopg2.connect(dbname=self.db, user=self.user, password=self.password, host=self.host, port=self.port)

	def get_cursor(self):
		self.cursor = self.connect.cursor()
		
	def disconnect_db(self):
		self.cursor.close()
		self.connect.close()
