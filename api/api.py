import time
from flask import Flask, request
from game import *

app = Flask(__name__)

@app.route('/time')
def get_current_time():
	return{'time': time.time()}


@app.route('/calculate/', methods=['GET'])
def calculate_move():
	fen_str = request.args.get('position')
	return return_move(fen_str)