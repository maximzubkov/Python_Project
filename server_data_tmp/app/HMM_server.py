import json
import math as m
import psycopg2
import sys
import numpy as np
from urllib.parse import urlparse
import socket	
import asyncio
import ast

sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/personal_info')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/markovs_chain/Python')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/server_data_tmp/app')
from personal_constants import *
from hmm import *
from obs import * 

CHUNK_TYPE_MOUSE = 0
CHUNK_TYPE_KEYBOARD = 1
WEBPAGE_TIME = 2
MAX_EVENTS_SIZE = 3
MAX_OBS_SIZE = 2
LEARN = 1
PREDICT = 2
LEARNED_ENOUGH = 50


class HMM(DB, hmm):
	def __init__(self, db, user, password, host, port, user_id):
		DB.__init__(self, db, user, password, host, port)
		self.get_connection()
		self.get_cursor()
		self.user_id = user_id

	def hmm_get_(self):
		SELECT_HMM = '''SELECT * FROM "hmm" WHERE "user_id" = {} '''.format(self.user_id)
		self.cursor.execute(SELECT_HMM)
		[(A, B, pi, self.status, tmp, ),] = self.cursor.fetchall()
		hmm.__init__(self, np.array(pi), np.array(A), np.array(B))

	def hmm_get_status(self):
		if self.status > LEARNED_ENOUGH:
			return PREDICT
		return LEARN

	def hmm_init_(self, unique_obs_len):
		a = (m.sqrt(unique_obs_len) * np.array([[0.5, 0.5] , [0.5, 0.5]])).tolist()
		r_1 = np.random.random(unique_obs_len)
		r_1 = (m.sqrt(unique_obs_len) * r_1 / np.sum(r_1)).tolist()
		r_2 = np.random.random(unique_obs_len)
		r_2 = (m.sqrt(unique_obs_len) * r_2 / sum(r_2)).tolist()
		b = np.array([r_1, r_2]).tolist()
		pi = (m.sqrt(unique_obs_len) * np.array([0.1, 0.9])).tolist()
		self.status = 0
		INSERT_HMM = '''INSERT INTO "hmm" (transition, emission, distribution, status, user_id) VALUES (array {}, array {}, array {}, 0, {});'''.format(a, b, pi, self.user_id)
		try:
			self.cursor.execute(INSERT_HMM)
			self.conn.commit()
		except:
			self.conn.rollback()
		hmm.__init__(self, np.array(pi), np.array(a), np.array(b))

	def hmm_update(self, obs_len):
		print("A", self.A, "B", self.B, "pi", self.pi)

		UPDATE_HMM = '''UPDATE "hmm" SET "transition" = array {}, "emission" = array {}, "distribution" = array {}, "status" = {} WHERE "user_id" = {}'''.format(self.A.tolist(), self.B.tolist(), self.pi.tolist(),  self.status + obs_len, self.user_id)
		try:
			self.cursor.execute(UPDATE_HMM)
			self.conn.commit()
		except:
			self.conn.rollback()
		self.hmm_get_()
	

	# def hmm_set(self, A = [[0.5, 0.5], [0.5, 0.5]], B = [[0.5, 0.5] for _ in range(100)], pi = [0.5, 0.5], obs_num = 0):
	# 	SET_HMM = '''UPDATE "hmm" SET "transition" = array {}, "emission" = array {}, "distribution" = array {}, "status" = {} WHERE "user_id" = {}'''.format(A, B, pi, self.status + obs_num, self.user_id)
	# 	try:
	# 		self.cursor.execute(SET_HMM)
	# 		self.conn.commit()
	# 	except:
	# 		self.conn.rollback()
	# 	self.hmm_get_()
	# 	print("A", self.A, "B", self.B, "pi", self.pi)

	def hmm_learn(self, obs):
		print(obs)
		self.hmm_init_(len(set(obs)))
		self.learn(obs)
		self.hmm_update(len(obs))
		print("updated")

	def hmm_predict(self, obs):
		print(obs)
		self.hmm_get_()
		path, prob = self.viterbi(obs)
		print(prob)



dictionary = {}

class ClientServerProtocol(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport
	
	def process_data(self, data):
		status, user_id, data = data[:-1].split(" ", 2)
		print(status, user_id)
		try:
			user_id = int(user_id)
			data = ast.literal_eval(data)
			if status not in ['learn', 'predict']:
				return "error\nwrong data\n\n"
		except:
			return "error\nwrong data\n\n"
		res = ""
		markov_model = HMM(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim, user_id)
		print(data)
		if status == 'predict':
			markov_model.hmm_predict(data)
			print("PREDICT")
		if status == 'learn':
			markov_model.hmm_learn(data)
			print("LEARN")

		# markov_model.hmm_predict(data)
		res += "ok\n\n"
		return res

	def data_received(self, data):
		resp = self.process_data(data.decode())
		self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

run_server("127.0.0.1", 8181)
