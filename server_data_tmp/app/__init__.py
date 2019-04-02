from flask import Flask,request, jsonify
from flask_jsonrpc import JSONRPC




app = Flask(__name__)
jsonrpc = JSONRPC(app,'/api')


@app.route('/')
def index():
    return "Template to recieve data"

@app.route('/api/get_content', methods=['GET', 'POST'])
def get_content():
	content = ("""{}\n\n""".format(request.get_json(force=True))).replace('\'','\"')
	with open('data_tmp.json','a') as file:
		file.write(content)
	return jsonify(content)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port= 5000)
