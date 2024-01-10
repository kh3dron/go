from flask import Flask, request, jsonify
from flask_cors import CORS

from dlgo import agent
from dlgo import goboard as goboard
from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.utils import *
from six.moves import input

import time

board_size = 9
game = goboard.GameState.new_game(board_size)


app = Flask(__name__)
CORS(app)


# TODO
@app.route('/place_stone', methods=['PUT'])
def place_stone():
    return jsonify(view_boardtiles(game.board))

@app.route('/get_board', methods=['GET'])
def get_game_state():
    return jsonify(view_boardtiles(game.board))

@app.route('/reset', methods=['GET'])
def reset():
    global game
    game = goboard.GameState.new_game(board_size)
    return jsonify(view_boardtiles(game))

@app.route('/gamestats', methods=['GET'])
def placed_stones():
    return stone_scores(game)

@app.route('/agent_random', methods=['GET'])
def agent_random():
    try:
        sleep_time = 0.2
        time.sleep(sleep_time)
        bot = RandomBot()
        move = bot.select_move(game)
        game = game.apply_move(move)
    except Exception as e:
        print("Agent Error:", e)

    return jsonify(view_boardtiles(game.board))

if __name__ == '__main__':
    app.run(port=3001, debug=True)