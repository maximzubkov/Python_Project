import psycopg2
import json
from datetime import datetime as dt
import sys



class DB():

	def __init__(self, db, user, password,host,port):
		self.db = db
		self.user = user
		self.password = password
		self.host = host
		self.port = port

	def get_connection(self):
		self.conn = psycopg2.connect(dbname=self.db, user=self.user, password=self.password, host=self.host, port=self.port)

	def get_cursor(self):
		self.cursor = self.conn.cursor()
		
	def disconnect_db(self):
		self.cursor.close()
		self.conn.close()





class Table(DB):

	def __init__(self, db, user, password, host,port, columns, table):
		super().__init__(db, user, password,host,port)
		self.table = table
		self.columns = columns
		self.get_connection()
		self.get_cursor()

	def get_columns_(self):
		SELECT_COLUMN = '''SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' and table_name = '{}' and column_default is null'''.format(table)
		self.cursor.execute(SELECT_COLUMN)
		self.columns = []
		for (tmp, ) in self.cursor.fetchall():
			self.columns.append(tmp)
		print(self.columns)

	def get_webpage_id_(self, table, user_id, url):
		SELECT_ID = "SELECT id FROM \"{}\" d WHERE d.url = {} AND d.user_id = {}".format(table, url, user_id)
		self.cursor.execute(SELECT_ID)
		[(web_id,),] = self.cursor.fetchall()

		if not web_id:
			Exception('no id found')	
		else:
			return web_id

	def count_varience_mouse(self):#TODO
		pass

	def count_varience_keyboard(self):#TODO
		pass

	def insert_new_observation(self):#TODO
		pass

	def to_csv(self, path):
		with open(path, 'a+') as file:
			self.cursor.copy_to(file, self.table, sep=',', null='NaN')


	def json_in_db (self, json_str):

		"""
			Закинуть информацию из имеющегося json-файла в базу данных
			TODO: тесты
		"""

		try:
			if self.cursor.closed == True:
				raise Exception('closed coursor')
		except:
			raise Exception('invalid coursor')

		try:
			json_str = (json_str).split('\n\n')
			for string in json_str:
				try:
					json_data = json.loads('''{}'''.format(string))
					if (json_data):
						for data in json_data:
							if (data):
								name = 'maxim'

								for columns_name in self.columns:
									if columns_name in data.keys():
										if isinstance(data[columns_name], str) :
											data[columns_name] = '\'' + data[columns_name] + '\''
										if columns_name == "keypress":
											data['keypress'] = 1
									else:
										data[columns_name] = 'NULL' 
								
								INSERT_USERS = '''INSERT INTO "users" (name) VALUES ('{}');'''.format(name)
								
								try:
									self.cursor.execute(INSERT_USERS)
									self.conn.commit()
								except:
									self.conn.rollback()
								
								SELECT_USERS_ID = "SELECT id FROM \"users\" u WHERE u.name = \'{}\'".format(name)
								self.cursor.execute(SELECT_USERS_ID)
								[(user_id,),] = self.cursor.fetchall()
			
								INSERT_WEB = '''INSERT INTO "webpage" (url, model, user_id) VALUES ({}, '{}', {});'''.format(data['current_page'], 'NEMA', user_id)
								
								try:
									self.cursor.execute(INSERT_WEB)
									self.conn.commit()
								except:
									self.conn.rollback()
								webpage_id = self.get_webpage_id_('webpage', user_id, data['current_page'])
								INSERT_DATA = '''INSERT INTO "data" ("webpage_id", "type", "positionX", 
																	 "positionY", "currentWidth", "currentHeight", 
																	 "minutes", "seconds", "miliseconds", "keypress", 
																	 "scrollPositionY", "scrollPositionX", "selectedText", 
																	 "shiftPress", "ctrlPress","time_on_page") 
																	 VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},{});'''.format(webpage_id, data['type'], data['positionX'], data['positionY'], data['currentWidth'], data['currentHeight'], data['minutes'], data['seconds'], data['miliseconds'], data['keypress'], data['scrollPositionY'], data['scrollPositionX'], data['selectedText'], data['shiftPress'], data['ctrlPress'],data['time_on_page'])
								self.cursor.execute(INSERT_DATA)
								self.conn.commit()
				except:
					Exception('invalid json')	
		except:
			raise Exception('invalid str')



