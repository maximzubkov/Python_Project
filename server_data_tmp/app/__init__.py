from flask import Flask,request, jsonify
from flask_jsonrpc import JSONRPC
import psycopg2
import sys
import config



app = Flask(__name__)
app.config.from_object(config.ProductionConfig)
jsonrpc = JSONRPC(app,'/api')

sys.path.insert(0,app.config['SQL_PATH'])
from sql_methods import *


		
@app.route('/')
def index():
    return "Template to recieve data"

@app.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
	content = ("""{}""".format(request.get_json(force=True))).replace('\'','\"')
	if content[0] != '[':
		content = '[' + content + ']'
	content += '\n\n'
	json_insert.json_in_db(content)
	return jsonify(content)

if __name__ == '__main__':
	columns = ['type', 'current_page', 'minutes', 'seconds', 'miliseconds', 'selectedText', 'currentHeight', 'currentWidth', 'scrollPositionY', 'scrollPositionX', 'keypress', 'shiftPress', 'ctrlPress', 'positionX', 'positionY',"time_on_page"]
	json_insert = Table(app.config['DB'], app.config['USER'], app.config['PASSWORD'], 
						app.config['HOST'], app.config['PORT'], 
						columns, 'data')
	app.run(host='127.0.0.1', port= 5000)
	# json_insert.to_csv('/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/son.csv')
	json_insert.disconnect_db()