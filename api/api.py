from flask import Flask, request
from game import *
from flask_cors import CORS, cross_origin

#app = Flask(__name__, static_folder='../build', static_url_path='/')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/')
# def index():
# 	return app.send_static_file('index.html')

@app.route('/')
def index():
	return '<h1>Deployed to Heroku!!</h1>'

@app.route('/api/calculate/', methods=['GET'])
@cross_origin()
def calculate_move():
	fen_str = request.args.get('position')
	response = return_move(fen_str)
	return response