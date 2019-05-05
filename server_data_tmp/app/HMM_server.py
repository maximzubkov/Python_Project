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


class HMM(DB, hmm):
	def __init__(self, db, user, password, host, port, user_id):
		DB.__init__(self, db, user, password, host, port)
		self.user_id = user_id
		self.hmm_get_()
		hmm.__init__(self, self.A, self.B, self.pi)
		print("A", self.A, "B", self.B, "pi", self.pi)

	def hmm_get_(self, user_id):
		SELECT_HMM = '''SELECT * FROM "hmm" WHERE "user_id" = {} '''.format(self.user_id)
		self.cursor.execute(SELECT_HMM)
		[(self.A, self.B, self.pi, tmp,),] = self.cursor.fetchall()

	def hmm_update(self, user_id):
		UPDATE_HMM = '''UPDATE "hmm" SET "transition" = array {}, "emission" = array {}, "distribution" = array {} WHERE "user_id" = {}'''.format(self.A, self.B, self.pi, user_id)
		try:
			self.cursor.execute(UPDATE_HMM)
			self.conn.commit()
		except:
			self.conn.rollback()

	def hmm_set(self, A, B, pi, user_id):
		SET_HMM = '''UPDATE "hmm" SET "transition" = array {}, "emission" = array {}, "distribution" = array {} WHERE "user_id" = {}'''.format(A, B, pi, user_id)
		try:
			self.cursor.execute(SET_HMM)
			self.conn.commit()
		except:
			self.conn.rollback()
		self.hmm_get_()
		print("A", self.A, "B", self.B, "pi", self.pi)

	def hmm_learn(self, obs):
		print(obs)
		self.learn(obs)
		self.hmm_update()

	def hmm_predict(self, obs):
		print(obs)
		path, prob = self.viterbi(obs)



dictionary = {}

class ClientServerProtocol(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport
	
	def process_data(self, data):
		print(data)
		action, user_id, data = data[:-1].split(" ", 2)
		try:
			user_id = int(user_id)
			data = ast.literal_eval(data)
		except:
			return "error\nwrong data\n\n"
		res = ""
		if action == "learn":
			print("lerning")
			markov_model = HMM(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim, user_id)
			# markov_model.hmm_learn(data)
			res += "ok\n\n"
			return res
        
        
		if action == "predict":
			print("predict")
			markov_model = HMM(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim, user_id)
			# markov_model.hmm_predict(data)
			res += "ok\n\n"
			return res
                
            
		if action != "learn" and action != "predict":
			return "error\nwrong command\n\n"
            
        
    
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
