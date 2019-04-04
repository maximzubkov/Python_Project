import psycopg2
import json
from datetime import datetime as dt

# def get_last_id_in_table(table, cursor):
# 	SELECT_ID = "SELECT id FROM \"{}\" d ORDER BY d.id DESC LIMIT 1;".format(table)
# 	cursor.execute(SELECT_ID)
# 	tmp = cursor.fetchall()
# 	if tmp:
# 		return tmp[0][0]
# 	else:
# 		return -1

def get_webpage_id_in_table(table, user_id, url, cursor):
	SELECT_ID = "SELECT id FROM \"{}\" d WHERE d.url = '{}' AND d.user_id = {}".format(table, url, user_id)
	cursor.execute(SELECT_ID)
	tmp = cursor.fetchall()
	if tmp:
		return tmp[0][0]
	else:
		print ("tupoi polzovatel")

def json_in_db (db = 'zumamotu', user = 'MaximZubkov', password='maxTBMzu', host = "localhost", port='1234', json_file = None , json_str = None):

	"""
		Закинуть информацию из имеющегося json-файла в базу данных
		TODO: тесты
	"""
	if not json_str and not json_file:
		print('TODO все плохо')

	json_file = 'data_tmp.json'
	with open(json_file, 'r') as f:
		with psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port) as conn:
			with conn.cursor() as cursor:
				json_str = (f.read()).split('\n\n')
				for string in json_str:
					try:
						json_data = json.loads('''{}'''.format(string))
						if (json_data):
							for info in json_data:
								if (info):
									name = 'maxim'
									event_type = info['type']
									current_page = info['current_page']
									minutes = info['minutes']
									seconds = info['seconds']
									data = info['data']
									if ('selectedText' in data.keys()):
										selectedText = data['selectedText']
									else:
										selectedText = 'NULL'
									if ('currentHeight' in data.keys()):
										currentHeight = data['currentHeight']
									else:
										currentHeight = 'NULL'
									if ('currentWidth' in data.keys()):
										currentWidth = data['currentWidth']
									else:
										currentWidth = 'NULL'
									if ('scrollPositionY' in data.keys()):
										scrollPositionY = data['scrollPositionY']
									else:
										scrollPositionY = 'NULL'
									if ('scrollPositionX' in data.keys()):
										scrollPositionX = data['scrollPositionX']
									else:
										scrollPositionX = 'NULL'
									if ('keypress' in data.keys()):
										keypress = '\'' + str(data['keypress']) + '\''
									else:
										keypress = 'NULL'
									if ('shiftPress' in data.keys()):
										shiftPress = data['shiftPress']
									else:
										shiftPress = 'NULL'
									if ('ctrlPress' in data.keys()):
										ctrlPress = data['ctrlPress']
									else:
										ctrlPress = 'NULL'
									if ('positionX' in data.keys()):
										positionX = data['positionX']
									else:
										positionX = 'NULL'
									if ('positionY' in data.keys()):
										positionY = data['positionY']
									else:
										positionY = 'NULL'
						
									INSERT_USERS = '''INSERT INTO "users" (name) VALUES ('{}');'''.format(name)
									
									try:
										cursor.execute(INSERT_USERS)
										conn.commit()
									except:
										conn.rollback()
									
									SELECT_USERS_ID = "SELECT id FROM \"users\" u WHERE u.name = \'{}\'".format(name)
									cursor.execute(SELECT_USERS_ID)
									tmp = cursor.fetchall()
									user_id = tmp[0][0]
							
									INSERT_WEB = '''INSERT INTO "webpage" (url, model, user_id) VALUES ('{}', '{}', {});'''.format(current_page, 'None', user_id)
									
									try:
										cursor.execute(INSERT_WEB)
										conn.commit()
									except:
										conn.rollback()

									webpage_id = get_webpage_id_in_table('webpage', user_id, current_page, cursor)
					
									INSERT_DATA = '''INSERT INTO "data" ("webpage_id", 
																		 "event_type", 
																		 "positionX", 
																		 "positionY", 
																		 "currentWidth", 
																		 "currentHeight", 
																		 "minutes", 
																		 "seconds", 
																		 "keypress", 
																		 "scrollPositionY", 
																		 "scrollPositionX", 
																		 "selectedText", 
																		 "shiftPress", 
																		 "ctrlPress") VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'''.format(webpage_id, event_type, positionX, positionY, currentWidth, currentHeight, minutes, seconds, keypress, scrollPositionY, scrollPositionX, selectedText, shiftPress, ctrlPress)
									cursor.execute(INSERT_DATA)
									conn.commit()
					except:
						print(1)	



json_in_db()