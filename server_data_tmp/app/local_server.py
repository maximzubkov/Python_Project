from flask import Flask,request, jsonify
from flask_jsonrpc import JSONRPC
# import json_to_db
import psycopg2
import sys
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/personal_info')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/server_data_tmp/app')
sys.path.insert(0,'/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/sql/')
from personal_constants import *
from obs import *


app = Flask(__name__)
jsonrpc = JSONRPC(app,'/api')


		
@app.route('/')
def index():
    return "Template to recieve data"

@app.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')

	if content != "[]" and content:
		if content[0] != '[':
			content = '[' + content + ']'
		content += '\n\n'
		print(content)
		# o.add_obs(content)
	# json_insert.json_in_db(content)
	return jsonify(content)

if __name__ == '__main__':
	o = obs(DB_maxim, USER_maxim, PASSWORD_maxim, HOST_maxim, PORT_maxim)
	app.run(host='127.0.0.1', port= 5000)
	# json_insert.to_csv('/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/son.csv')
	o.disconnect_db()