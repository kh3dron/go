from flask import Flask, request, jsonify
from flask_cors import CORS

from dlgo import agent
from dlgo import goboard as goboard
from dlgo import gotypes
from dlgo.agent.naive import RandomBot
from dlgo.utils import *
from six.moves import input

import time

board_size = 5
game = goboard.GameState.new_game(board_size)


app = Flask(__name__)
CORS(app)

@app.route('/place_stone', methods=['PUT'])
def place_stone():
    global game
    p = request.json.get('move')
    coords = goboard.Move.play(gotypes.Point(row=(board_size - p["row"]), col=(p["col"] + 1)))

    if not game.is_valid_move(coords):
        print("Invalid move")
        return jsonify(view_boardtiles(game.board))

    try:
        game = game.apply_move(coords)
        return jsonify(view_boardtiles(game.board))
    except Exception as e:
        print("Error applying move:", e)
        return jsonify(view_boardtiles(game.board)), 500


@app.route("/pass", methods=['PUT'])
def pass_turn():
    global game
    game = game.apply_move(goboard.Move.pass_turn())
    return jsonify(view_boardtiles(game.board))

@app.route('/get_board', methods=['GET'])
def get_game_state():
    global game
    return jsonify(view_boardtiles(game.board))

@app.route('/reset', methods=['GET'])
def reset():
    global game
    newgame = goboard.GameState.new_game(board_size)
    game = newgame
    return jsonify(view_boardtiles(game.board))

@app.route('/gamestats', methods=['GET'])
def placed_stones():
    global game
    return jsonify(stone_scores(game))

@app.route('/agent_random', methods=['GET'])
def agent_random():
    global game
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
