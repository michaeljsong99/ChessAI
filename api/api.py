from flask import Flask, request
from game import *

#app = Flask(__name__, static_folder='../build', static_url_path='/')
app = Flask(__name__)

# @app.route('/')
# def index():
# 	return app.send_static_file('index.html')

@app.route('/')
def index():
	return '<h1>Deployed to Heroku!!</h1>'

@app.route('/api/calculate/', methods=['GET'])
def calculate_move():
	fen_str = request.args.get('position')
	return return_move(fen_str)