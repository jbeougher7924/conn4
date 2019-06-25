# importing Flask
from flask import Flask, jsonify, render_template, request

import json
# import tic tac toe game 
from deep_reinforcement_learningV2 import *

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

game_rows = rows = ROW_COUNT
game_cols = cols = COLUMN_COUNT
winning_length = 3
boardSize = rows * cols
actions = rows * cols
won_games = 0
lost_games = 0
draw_games = 0
layer_1_w = 750
layer_2_w = 750
layer_3_w = 750


EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

game_loop = False
current_player = 1
player_move = None

token_used_cols_np = np.full(shape=cols, fill_value=(0), dtype=int)

board_list_np = np.array([0] * (rows * cols)).reshape(rows, cols)


# setting up session
sess = tf.InteractiveSession()
# prediction = neural_network_model(x)
x, prediction, _ = createNetwork()
# prediction = convolutional_neural_network(x)
saver = tf.train.Saver()
checkpoint = tf.train.get_checkpoint_state("model")
if checkpoint and checkpoint.model_checkpoint_path:
    s = saver.restore(sess,checkpoint.model_checkpoint_path)
    print("Successfully loaded the model:", checkpoint.model_checkpoint_path)
else:
    print("Could not find old network weights")
graph = tf.get_default_graph()


def  bestmove(input):
    global graph
    with graph.as_default():
        data = (sess.run(tf.argmax(prediction.eval(session = sess,feed_dict={x:[input]}),1)))
    return data


def print_board():
    label = -1
    for row in range(rows):
        col0 = board_list_np[row, 0]
        col1 = board_list_np[row, 1]
        col2 = board_list_np[row, 2]
        col3 = board_list_np[row, 3]
        col4 = board_list_np[row, 4]
        col5 = board_list_np[row, 5]
        col6 = board_list_np[row, 6]
        label += 7
        print("{} {} {} {} {} {} {} {}".format(col0, col1, col2, col3, col4, col5, col6, label))


def print_tokensUsed():
    print(token_used_cols_np)


# def place_token(column, player):
#     if token_used_cols_np[column] <= 6:
#         print("row: {} col: {}".format(column, token_used_cols_np[column]))
#         board_list_np[column, token_used_cols_np[column]] = player
#         token_used_cols_np[column] += 1
#         return True
#     else:
#         return False

# def place_token(column, player):
#     if token_used_cols_np[column] >= 0:
#         board_list_np[column, token_used_cols_np[column]] = player
#         token_used_cols_np[column] -= 1
#         return True
#     else:
#         return False

def place_token(column, player):
    if token_used_cols_np[column] <= 6:
        print("row: {} col: {}".format( token_used_cols_np[column], column))
        board_list_np[token_used_cols_np[column], column] = player
        token_used_cols_np[column] += 1
        return True
    else:
        return False


if __name__ == '__main__':
    # app.run(host='127.0.0.1',port=80,debug=True)
    # board = board_list_np.reshape(1,42).tolist()
    # print(np.asscalar(bestmove(board[0])))
    # print(board[0])
    # board_list_np[0, 0] = 1


    player = int(input("1 or -1"))
    # player = 1
    place_maker = 0
    while True:

        print_board()


        place_maker = int(input("drop token player: {}".format(player)))

        place_token(place_maker,player)
        if player == 1:
            player = -1
        else:
            player = 1
        board = board_list_np.reshape(1,42).tolist()
        print("Best Move: {}".format(np.asscalar(bestmove(board[0]))))
