import numpy as np
import math
cols = 7
rows = 6
board_size = cols * rows
board_phase_count = 0

game_loop = False
current_player = 1
player_move = None

token_used_cols_np = np.full(shape=cols, fill_value=(rows - 1), dtype=int)

board_list_np = np.zeros(shape=(board_size, cols, rows), dtype=int)


def place_token(board_phase, column, player):
    if token_used_cols_np[column] >= 0:
        for i in range(board_phase, board_size):
            board_list_np[i, column, token_used_cols_np[column]] = player
        token_used_cols_np[column] -= 1
        return True
    else:
        return False


def print_board(board_phase):
    for row in range(rows):
        col0 = board_list_np[board_phase,  0, row]
        col1 = board_list_np[board_phase,  1, row]
        col2 = board_list_np[board_phase,  2, row]
        col3 = board_list_np[board_phase,  3, row]
        col4 = board_list_np[board_phase,  4, row]
        col5 = board_list_np[board_phase,  5, row]
        col6 = board_list_np[board_phase,  6, row]
        print("{} {} {} {} {} {} {}".format(col0, col1, col2, col3, col4, col5, col6))

def print_tokensUsed():
    print(token_used_cols_np)


def checkWin(board_phase, player):

    for col in range(cols - 3):
        for row in range(3, rows):
            spot1 = board_list_np[board_phase, col, row ]
            spot2 = board_list_np[board_phase, col + 1, row - 1]
            spot3 = board_list_np[board_phase, col + 2, row - 2]
            spot4 = board_list_np[board_phase, col + 3, row - 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols - 3):
        for row in range(rows - 3):
            spot1 = board_list_np[board_phase, col, row ]
            spot2 = board_list_np[board_phase, col + 1, row + 1]
            spot3 = board_list_np[board_phase, col + 2, row + 2]
            spot4 = board_list_np[board_phase, col + 3, row + 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols):
        for row in range(rows - 3):
            spot1 = board_list_np[board_phase, col, row ]
            spot2 = board_list_np[board_phase, col, row + 1]
            spot3 = board_list_np[board_phase, col, row + 2]
            spot4 = board_list_np[board_phase, col, row + 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols - 3):
        for row in range(rows):
            spot1 = board_list_np[board_phase, col, row ]
            spot2 = board_list_np[board_phase, col + 1, row]
            spot3 = board_list_np[board_phase, col + 2, row]
            spot4 = board_list_np[board_phase, col + 3, row]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True
    return False


if __name__ == "__main__":
    while not game_loop:
        player_move = int(input("Player: {} Enter number 1 to 7 \n".format(current_player))) - 1

        while not place_token(board_phase_count, player_move, current_player):
            print_board()
            print("This column is full choose another column")
            player_move = int(input("Player: {} Enter number 1 to 7 \n".format(current_player))) - 1

        game_loop = checkWin(board_phase_count, current_player)
        if not game_loop:
            print_board(board_phase_count)
            if current_player == 1:
                current_player = 2
            else:
                current_player = 1
        else:
            print("Game Over Player {} Won".format(current_player))

    print_board(board_phase_count)