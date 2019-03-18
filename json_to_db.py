import psycopg2
import json
from datetime import datetime as dt

def get_last_id_in_table(table, cursor):
	SELECT_ID = "SELECT id FROM \"{}\" d ORDER BY d.id DESC LIMIT 1;".format(table)
	cursor.execute(SELECT_ID)
	tmp = cursor.fetchall()
	if tmp:
		return tmp[0][0]
	else:
		return -1

def json_in_db (db = 'zumamotu', user = 'MaximZubkov', password='maxTBMzu', host = "localhost", port='1234', json_file = 'tmp.txt'):

	"""
		Закинуть информацию из имеющегося json-файла в базу данных
		TODO: тесты
	"""
	
	with psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port) as conn:
		with conn.cursor() as cursor:
			with open(json_file, 'r') as f:
				json_str = (f.read()).split('\n\n')
				i = 0;
				for string in json_str:
					json_data = json.loads(string)
					name = json_data['name']
					url = json_data['url']
					data = json_data['data']
					data_x = data['x']
					data_y = data['y']
					data_w = data['w']
					data_h = data['h']
					data_isClick = data['isClick']
					data_ts = data['ts']
					SELECT_USERS_ID = "SELECT id FROM \"users\" u WHERE u.name = \'{}\'".format(name)
					cursor.execute(SELECT_USERS_ID)
					tmp = cursor.fetchall()
					if not tmp:
						user_id = get_last_id_in_table('users', cursor) + 1
						INSERT_USERS = '''INSERT INTO "users" (id, name) VALUES ({}, '{}');'''.format(user_id, name)
						cursor.execute(INSERT_USERS)
						conn.commit()
					else:
						user_id = tmp[0][0]
					
					webpage_id = get_last_id_in_table('webpage', cursor) + 1
					INSERT_WEB = '''INSERT INTO "webpage" (id, url, model, user_id) VALUES ({}, '{}', '{}', {});'''.format(webpage_id, url, 'None', user_id )
					data_id = get_last_id_in_table('data', cursor) + 1
					INSERT_DATA = '''INSERT INTO "data" (id, webpage_id, x, y, w, h, is_click, ts) VALUES ({}, {}, {}, {}, {}, {}, {}, TIMESTAMP '{}');'''.format(data_id, webpage_id, data_x, data_y, data_w, data_h, data_isClick, dt.now())
					cursor.execute(INSERT_WEB)
					conn.commit()
					cursor.execute(INSERT_DATA)
					conn.commit()

json_in_db()