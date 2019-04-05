from flask import Flask,request, jsonify
from flask_jsonrpc import JSONRPC
# import json_to_db
import psycopg2
import sys
sys.path.insert(0,'../../personal_info')
sys.path.insert(0,'../../sql')
from personal_constants import *
from sql_methods import *
import psycopg2



app = Flask(__name__)
jsonrpc = JSONRPC(app,'/api')


		
@app.route('/')
def index():
    return "Template to recieve data"

@app.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')
	if content[0] != '[':
		content = '[' + content + ']'
		print(content)
	content += '\n\n'
	with open('data_tmp.json','a') as file:
		file.write(content)
	return jsonify(content)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port= 5000)
