from flask import Flask, request, jsonify
from flask_jsonrpc import JSONRPC
import psycopg2
import sys
import config
import pandas as pd
from flask_script import Manager,Server


app = Flask(__name__)
app.config.from_object(config.ProductionConfig)
jsonrpc = JSONRPC(app,'/api')
manager = Manager(app)

sys.path.insert(0,app.config['SCRIPTS_PATH'])
from file_utils import insert_history_to_file

sys.path.insert(0,app.config['CLIENT_CLASS'])
from obs import *

		
@app.route('/')
def index():
    return "Template to recieve data"

@app.route('/api/get_history', methods=['GET', 'POST'])
def get_history():
	content = request.get_json(force=True)
	# print(content)
	client.learn(content)
	return jsonify(200)

@app.route('/api/get_login', methods=['GET', 'POST'])
def get_login():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')
	print(content)
	client.create_user(content)
	return jsonify(content)

@app.route('/api/get_password', methods=['GET', 'POST'])
def get_password():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')
	print(content)
	client.login(content)
	return jsonify(content)

@app.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')
	print(content)
	if content != "[]" and content:
		if content[0] != '[':
			content = '[' + content + ']'
		content += '\n\n'
		# print(content)
		client.put(content)
	# json_insert.json_in_db(content)
	return jsonify(content)

with app.app_context():
	client = Client("127.0.0.1", 8181, app.config['DB'], app.config['USER'], app.config['PASSWORD'], app.config['HOST'], app.config['PORT'])

#class CustomServer(Server):
  #  def __call__(self, app, *args, **kwargs):
 #       client = custom_call()
        #Hint: Here you could manipulate app
#        return Server.__call__(self, app)




if __name__ == '__main__':
	app.run(debug=True)



