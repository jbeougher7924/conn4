import numpy as np
import math
import random
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
    print("Turn: {}".format(board_phase))
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


def human_turn(player):

    human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1

    while not place_token(board_phase_count, human_move, player):
        print_board(board_phase_count)
        print("This column is full choose another column")
        human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1



def is_valid_location(board, col):
    return board[rows - 1][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(cols):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def ai_turn():
    pass


def switch_player(player, game_status):
    if not game_status:
        print_board(board_phase_count)

        if player == 1:
            player = 2
        else:
            player = 1
    else:
        print("Game Over Player {} Won".format(player))
    return player


if __name__ == "__main__":

    ai_players = False  # bool(int(input("Enter One or Zero for number of AI players.\n")))
    current_player = np.random.randint(1, 3)
    if ai_players:
        while not game_loop:
            if current_player == 1:
                human_turn(current_player)
            else:
                human_turn(current_player)

            game_loop = checkWin(board_phase_count, current_player)
            current_player = switch_player(current_player, game_loop)
            board_phase_count += 1

    else:
        while not game_loop:
            human_turn(current_player)
            game_loop = checkWin(board_phase_count, current_player)
            current_player = switch_player(current_player, game_loop)
            board_phase_count += 1

    print_board(board_phase_count)
