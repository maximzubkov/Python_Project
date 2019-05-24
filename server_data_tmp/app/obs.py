import json
import math as m
import psycopg2
import sys
import numpy as np
from urllib.parse import urlparse
import socket	
import config 

paths = config.Path('production')
sys.path.insert(0, paths.markov_chain())

CHUNK_TYPE_MOUSE = 0
CHUNK_TYPE_KEYBOARD = 1
WEBPAGE_TIME = 2
MAX_EVENTS_SIZE = 3
MAX_OBS_SIZE = 10
LEARN = 1
PREDICT = 2
BLOCKED = 1
UNBLOCKED = 0

class DbWebPageError(Exception):
	pass
	
class DbUserError(Exception):
	pass

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



class obs(DB):
	def __init__(self, db, user, password, host, port):
		super().__init__(db, user, password, host, port)
		self.get_connection()
		self.get_cursor()
		self.velocity = dict()
		self.click_speed = dict()
		self.obs = dict()

	def velocity_model_(self, velocity_var):
		print(velocity_var)
		return round(velocity_var) % 2
		
	def click_model_(self, click_speed_mean):
		print(click_speed_mean)
		return round(click_speed_mean) % 2

	def time_count_(self, data_json):
		return data_json['minutes'] * 60 + data_json['seconds'] + data_json['miliseconds'] * 0.001

	def get_max_user_id_(self):
		MAX_ID = '''SELECT MAX(id) FROM "users" '''
		self.cursor.execute(MAX_ID)
		[(max_id,),] = self.cursor.fetchall()
		return max_id

	def get_max_webpage_id_(self, name = 'maxim'):
		user_id = self.get_user_id_(name)
		MAX_ID = '''SELECT MAX(id) FROM "webpage" w WHERE w.user_id = {} '''.format(user_id)
		self.cursor.execute(MAX_ID)
		[(max_id,),] = self.cursor.fetchall()
		if not max_id:
			return 0	
		else:
			return max_id

	def get_user_id_(self, name = 'maxim'):
		SELECT_USERS_ID = '''SELECT id FROM "users" u WHERE u.name = '{}' '''.format(name)
		self.cursor.execute(SELECT_USERS_ID)
		[(user_id,),] = self.cursor.fetchall()
		if not user_id:
			Exception('no id found')	
		else:
			return user_id

	def web_page_(self, data_json, user_id):
		# TODO для многих пользователей
		web_id = self.get_max_webpage_id_() + 1
		INSERT_WEB = '''INSERT INTO "webpage" (id, url, model, user_id, time_on_page) VALUES ({}, '{}', '{}', {}, {});'''.format(web_id, data_json['current_page'], 'NEMA', user_id, 0)
		try:
			self.cursor.execute(INSERT_WEB)
			self.conn.commit()
		except:
			self.conn.rollback()
			print('web problem')

	def web_page_insert_(self, url, web_id, user_id):
		INSERT_WEB = '''INSERT INTO "webpage" (id, url, model, user_id, time_on_page) VALUES ({}, '{}', '{}', {}, {});'''.format(web_id, url, 'NEMA', user_id, 0)
		try:
			self.cursor.execute(INSERT_WEB)
			self.conn.commit()
		except:
			self.conn.rollback() 
			print('web problem')

	def get_webpage_id_(self, user_id, url):
		SELECT_ID = '''SELECT id FROM "webpage" w WHERE w.url = '{}' AND w.user_id = {}'''.format(url, user_id)
		self.cursor.execute(SELECT_ID)
		[(web_id,),] = self.cursor.fetchall()

		if not web_id:
			raise Exception("incorrect webpage")
		else:
			return web_id

	def get_obs_seq_(self, user_id):
		obs_seq = []
		for web_id in self.obs[user_id].keys():
			for obs in self.obs[user_id][web_id]:
				print(web_id, obs['velocity'], obs['click'])
				obs_seq.append(web_id)
				# obs_seq.append((web_id << 2) + (obs['velocity'] << 1) + obs['click'])
		return obs_seq

	def add_obs(self, json_str):
		prev_x = -1
		prev_y = -1
		prev_time = -1
		prev_click_time = -1
		user_id = -1
		web_page_id = -1
		json_str = (json_str).split('\n\n')
		json_str.remove('')
		for string in json_str:
			try:
				json_data = json.loads('''{}'''.format(string))
				for event in json_data:
					if user_id == -1:
						url = urlparse(event['current_page'])
						event['current_page'] = url.netloc + url.path

						user_id = self.get_user_id_(event['login'])

						self.web_page_(event, user_id)
						web_page_id = self.get_webpage_id_(user_id, event['current_page'])

						print("here we gooo", user_id, web_page_id, event['current_page'])
						
						if user_id in self.obs.keys():
							if web_page_id not in self.obs[user_id].keys():
								self.obs[user_id][web_page_id] = []
								self.velocity[user_id][web_page_id] = []
								self.click_speed[user_id][web_page_id] = []
						else:
							self.obs[user_id] = dict()
							self.obs[user_id][web_page_id] = []
							self.velocity[user_id] = dict()
							self.velocity[user_id][web_page_id] = []
							self.click_speed[user_id] = dict()
							self.click_speed[user_id][web_page_id] = []

					if event['type'] == CHUNK_TYPE_MOUSE:
						if prev_time != -1:
							self.velocity[user_id][web_page_id].append(m.sqrt((event['positionX'] - prev_x) ** 2 +  
								(event['positionY'] - prev_y) ** 2) / (self.time_count_(event) - prev_time))
				
						prev_time = self.time_count_(event)
						prev_x = event['positionX']
						prev_y = event['positionY']

					if event['type'] == CHUNK_TYPE_KEYBOARD:	
						if prev_click_time != -1:
							self.click_speed[user_id][web_page_id].append(self.time_count_(event) - prev_click_time)
						
						prev_click_time = self.time_count_(event)

					if event['type'] == WEBPAGE_TIME:
						SELECT_TIME = '''SELECT time_on_page FROM "webpage" w WHERE w.id = {} AND w.user_id = {}'''.format(web_page_id, user_id)
						self.cursor.execute(SELECT_TIME)
						[(time,),] = self.cursor.fetchall()
						# print(float(event['time_on_page']) + time)
						UPDATE_TIME = '''UPDATE "webpage" SET "time_on_page" = {} WHERE "id" = {} AND "user_id" = {}'''.format(time + float(event['time_on_page']), web_page_id, user_id)
						try:
							self.cursor.execute(UPDATE_TIME)
							self.conn.commit()
						except:
							self.conn.rollback()

						

			except:
				raise Exception('invalid json')	
		try:
			if (self.velocity[user_id][web_page_id] or self.click_speed[user_id][web_page_id]) and (len(self.velocity[user_id][web_page_id]) + len(self.click_speed[user_id][web_page_id]) > MAX_EVENTS_SIZE):
				print(user_id, web_page_id)
				self.obs[user_id][web_page_id].append({'click': int(self.click_model_(np.array(self.click_speed[user_id][web_page_id]).mean())), 'velocity': int(self.velocity_model_(np.array(self.velocity[user_id][web_page_id]).var()))})
				print(1111)
		except:
			print(json_str)
		return user_id
		# class learn(DB):
		# SELECT = '''SELECT * FROM "hmm" WHERE "user_id" = 1 '''
		# self.cursor.execute(SELECT)
		# [(A, B, pi, tmp,),] = self.cursor.fetchall()
		# print("A", A, "B", B, "pi", pi)
# 		UPDATE_TEST = '''UPDATE "test" SET "matrix" = array {} WHERE "id" = 1'''.format([[1, 2],[1,8]])
# 		try:
# 			self.cursor.execute(UPDATE_TEST)
# 			self.conn.commit()
# 		except:
# 			self.conn.rollback()

		# print(self.obs)

class ClientError(Exception):
	"""Общий класс исключений клиента"""
	pass


class ClientSocketError(ClientError):
	"""Исключение, выбрасываемое клиентом при сетевой ошибке"""
	pass


class ClientProtocolError(ClientError):
	"""Исключение, выбрасываемое клиентом при ошибке протокола"""
	pass


class Client(obs):
	def __init__(self, host, port, db, db_user, db_password, db_host, db_port, timeout=None):
		# класс инкапсулирует создание сокета
		# создаем клиентский сокет, запоминаем объект socke.socket в self 
		super().__init__(db, db_user, db_password, db_host, db_port)
		self.host = host
		self.port = port
		try:
			self.connection = socket.create_connection((host, port), timeout)
		except socket.error as err:
			raise ClientSocketError("error create connection", err)
		 
	def _read(self):
		"""Метод для чтения ответа сервера"""
		data = b""
		# накапливаем буфер, пока не встретим "\n\n" в конце команды
		while not data.endswith(b"\n\n"):
			try:
				data += self.connection.recv(1024)
				print(data)
			except socket.error as err:
				raise ClientSocketError("error recv data", err)

		# не забываем преобразовывать байты в объекты str для дальнейшей работы
		decoded_data = data.decode()

		status, payload = decoded_data.split("\n", 1)

		# если получили ошибку - бросаем исключение ClientError
		if status == "error":
			raise ClientProtocolError(payload)

		return payload

	def learn(self, data, user = 'maxim'):
		event = []
		print(data)
		self.user_(user)
		user_id = self.get_user_id_(user)
		for elem in data:
			url = urlparse(elem['url'])
			event.append(url.netloc + url.path)
		indexing = dict()
		i = 0
		for e in event[:-1]:
			if e not in indexing.keys():
				indexing[e] = i
				self.web_page_insert_(e, i + 1, user_id)
				i += 1

		obs_seq = []
		for web_page in event[:-1]:
			obs_seq.append(indexing[web_page])

		self.connection.sendall("learn {} {}\n".format(user_id, obs_seq).encode())
		print(self._read())

	def put(self, json_str):
		# отправляем запрос команды put
		# иногда ошибается
		user_id = self.add_obs(json_str)
		count = 0
		for wp_id in self.obs[user_id].keys():
			count += len(self.obs[user_id][wp_id])
		if count > MAX_OBS_SIZE:
			obs_seq = self.get_obs_seq_(user_id)
			print(obs_seq)
			for wp_id in self.obs[user_id].keys():
				self.obs[user_id][wp_id] = []
				self.velocity[user_id][wp_id] = []
				self.click_speed[user_id][wp_id] = []
			try:
				self.connection.sendall("predict {} {}\n".format(user_id, obs_seq).encode())
			except socket.error as err:
				raise ClientSocketError("error send data", err)
			# разбираем ответ
			print(self._read())
		return -1

	def close(self):
		try:
			self.connection.close()
			self.disconnect_db()
		except socket.error as err:
			raise ClientSocketError("error close connection", err)


	def setval_(self, table, max_id):
		SETVAL = '''SELECT setval('{}_id_seq',{})'''.format(table, max_id)
		
		try:
			self.cursor.execute(SETVAL)
			self.conn.commit()
		except:
			self.conn.rollback()

	def user_(self, name = 'maxim'):
		INSERT_USERS = '''INSERT INTO "users" (name) VALUES ('{}', NULL, 0);'''.format(name)
		try:
			self.cursor.execute(INSERT_USERS)
			self.conn.commit()
			user_id = self.get_user_id_(name)
			print(user_id)
		except:
			self.conn.rollback()
			max_id = self.get_max_user_id_()
			self.setval_("users", max_id)

	def create_password(self, login, password):
		UPDATE_STATUS = '''UPDATE "users" SET "password" = '{}', "status" = 0 WHERE "name" = '{}' '''.format(password, login)
		try:
			self.cursor.execute(UPDATE_STATUS)
			self.conn.commit()
		except:
			self.conn.rollback()

	def create_user(self, json_str):
		try:
			json_data = json.loads('''{}'''.format(json_str))
			login = json_data['login']
			print(login)
			self.user_(name)

		except:
			raise Exception("invalid json")

	def sign_up(self, json_str):
		try:
			json_data = json.loads('''{}'''.format(json_str))
			login = json_data['login']
			password = json_data['pass']
			print(login, password)
			self.create_password(login, password)

		except:
			raise Exception("invalid json")

	def change_status_(self, user, cur_status):
		UPDATE_STATUS = '''UPDATE "users" SET "status" = {} WHERE "name" = '{}' '''.format(not cur_status, user)
		try:
			self.cursor.execute(UPDATE_STATUS)
			self.conn.commit()
		except:
			self.conn.rollback()

	def check_user_(self, user, password):
		SELECT_USER_INFO = '''SELECT * FROM "users" u WHERE u.name = '{}' and '''.format(user)
		self.cursor.execute(SELECT_USER_INFO)
		[(user_id, user_password, user_status,),] = self.cursor.fetchall()
		if not user_id or not user_password or not user_status:
			raise Exception("invalid user")	
		else:
			if password == user_password:
				self.change_status_(user, UNBLOCK)
				return True
			else:
				if user_status == UNBLOCKED:
					self.change_status_(user, BLCOK)
					return False

	def sign_in(self, json_str):
		try:
			json_data = json.loads('''{}'''.format(json_str))
			login = json_data['login']
			if (self.check_user_(login)):
				pass
				# слать что-нибудь куда-нибудь
		except:
			raise Exception("invalid json")



# def _main():
#     # проверка работы клиента
#     client = Client("127.0.0.1", 8181, DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim)
#     client.put("learn", '''[{"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 58, "miliseconds": 957, "positionX": 632, "positionY": 682}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 39, "positionX": 745, "positionY": 258}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 80, "positionX": 750, "positionY": 197}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 111, "positionX": 682, "positionY": 316}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 120, "positionX": 619, "positionY": 480}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 129, "positionX": 613, "positionY": 505}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 142, "positionX": 604, "positionY": 561}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 158, "positionX": 604, "positionY": 588}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 174, "positionX": 612, "positionY": 614}, {"type": 0, "current_page": "https://vk.com/feed", "minutes": 32, "seconds": 59, "miliseconds": 192, "positionX": 651, "positionY": 606}]\n\n''')
#     client.close()


# if __name__ == "__main__":
#     _main()


# o = obs(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim)
# s = '[{"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 680, "positionX": 498, "positionY": 278}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 685, "positionX": 518, "positionY": 283}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 714, "positionX": 573, "positionY": 294}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 720, "positionX": 594, "positionY": 294}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 739, "positionX": 636, "positionY": 292}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 755, "positionX": 672, "positionY": 279}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 772, "positionX": 702, "positionY": 252}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 788, "positionX": 716, "positionY": 217}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 804, "positionX": 715, "positionY": 184}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 822, "positionX": 700, "positionY": 163}]'
# s = s.replace('\'','\"')
# if s[0] != '[':
# 	s = '[' + s + ']'
# s += '\n\n'
# # print(s)
# o.add_obs(s)
# h = HMM(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim, 1)
# h.hmm_set([[3,4],[6,7]], [[33, 44],[11,454]], [0.8, 0.8])
