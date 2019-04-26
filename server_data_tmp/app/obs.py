import json
import math as m
import psycopg2
import sys
import numpy as np
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/personal_info')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/markovs_chain/Python')
from personal_constants import *
from hmm import *

CHUNK_TYPE_MOUSE = 0
CHUNK_TYPE_KEYBOARD = 1
MAX_EVENTS_SIZE = 3
MAX_OBS_SIZE = 2

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
		super().__init__(db, user, password,host,port)
		self.get_connection()
		self.get_cursor()
		self.velocity = dict()
		self.click_speed = dict()
		self.obs = dict()

	def velocity_model_(self, velocity_var):
		return round(velocity_var) % 2
	def click_model_(self, click_speed_mean):
		return round(click_speed_mean) % 2
	def time_count_(self, data_json):
		return data_json['minutes'] * 60 + data_json['seconds'] + data_json['miliseconds'] * 0.001

	def user_(self, name = 'maxim'):
		INSERT_USERS = '''INSERT INTO "users" (name) VALUES ('{}');'''.format(name)
		
		try:
			self.cursor.execute(INSERT_USERS)
			self.conn.commit()
		except:
			self.conn.rollback()
		
	def get_user_id_(self, name = 'maxim'):
		SELECT_USERS_ID = '''SELECT id FROM "users" u WHERE u.name = '{}' '''.format(name)
		self.cursor.execute(SELECT_USERS_ID)
		[(user_id,),] = self.cursor.fetchall()
		if not user_id:
			Exception('no id found')	
		else:
			return user_id

	def web_page_(self, data_json, user_id):
		INSERT_WEB = '''INSERT INTO "webpage" (url, model, user_id) VALUES ('{}', '{}', {});'''.format(data_json['current_page'], 'NEMA', user_id)
		try:
			self.cursor.execute(INSERT_WEB)
			self.conn.commit()
		except:
			self.conn.rollback()

	def get_webpage_id_(self, user_id, url):
		SELECT_ID = '''SELECT id FROM "webpage" d WHERE d.url = '{}' AND d.user_id = {}'''.format(url, user_id)
		self.cursor.execute(SELECT_ID)
		[(web_id,),] = self.cursor.fetchall()

		if not web_id:
			Exception('no id found')	
		else:
			return web_id

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
						self.user_()
						user_id = self.get_user_id_()

						self.web_page_(event, user_id)
						web_page_id = self.get_webpage_id_(user_id, event['current_page'])
						
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

			except:
				Exception('invalid json')	
		if self.velocity[user_id][web_page_id] and self.click_speed[user_id][web_page_id] and (len(self.velocity[user_id][web_page_id]) + len(self.click_speed[user_id][web_page_id]) > MAX_EVENTS_SIZE):
			self.obs[user_id][web_page_id].append({'click': int(self.click_model_(np.array(self.click_speed[user_id][web_page_id]).mean())), 
				'velocity': int(self.velocity_model_(np.array(self.velocity[user_id][web_page_id]).var()))})
		if len(self.obs[user_id][web_page_id]) > MAX_OBS_SIZE:
			pass
		print(self.obs)


# o = obs(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim)
# s = '[{"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 680, "positionX": 498, "positionY": 278}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 685, "positionX": 518, "positionY": 283}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 714, "positionX": 573, "positionY": 294}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 720, "positionX": 594, "positionY": 294}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 739, "positionX": 636, "positionY": 292}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 755, "positionX": 672, "positionY": 279}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 772, "positionX": 702, "positionY": 252}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 788, "positionX": 716, "positionY": 217}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 804, "positionX": 715, "positionY": 184}, {"type": 0, "current_page": "https://www.google.com/search?q=vl&oq=vl&aqs=chrome.0.69i59j0j69i60j0l3.667j0j9&sourceid=chrome&ie=UTF-8", "minutes": 46, "seconds": 50, "miliseconds": 822, "positionX": 700, "positionY": 163}]'
# s = s.replace('\'','\"')
# if s[0] != '[':
# 	s = '[' + s + ']'
# s += '\n\n'
# # print(s)
# o.add_obs(s)


