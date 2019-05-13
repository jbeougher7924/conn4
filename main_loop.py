import numpy as np
import math
import random
cols = 7
rows = 6
board_size = cols * rows
board_phase_count = 0

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

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


def checkWin(board, board_phase, player):
    # print("Turn: {}".format(board_phase))
    for col in range(cols - 3):
        for row in range(3, rows):
            spot1 = board[board_phase, col, row ]
            spot2 = board[board_phase, col + 1, row - 1]
            spot3 = board[board_phase, col + 2, row - 2]
            spot4 = board[board_phase, col + 3, row - 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols - 3):
        for row in range(rows - 3):
            spot1 = board[board_phase, col, row ]
            spot2 = board[board_phase, col + 1, row + 1]
            spot3 = board[board_phase, col + 2, row + 2]
            spot4 = board[board_phase, col + 3, row + 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols):
        for row in range(rows - 3):
            spot1 = board[board_phase, col, row ]
            spot2 = board[board_phase, col, row + 1]
            spot3 = board[board_phase, col, row + 2]
            spot4 = board[board_phase, col, row + 3]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True

    for col in range(cols - 3):
        for row in range(rows):
            spot1 = board[board_phase, col, row ]
            spot2 = board[board_phase, col + 1, row]
            spot3 = board[board_phase, col + 2, row]
            spot4 = board[board_phase, col + 3, row]
            if spot1 == player and spot2 == player and spot3 == player and spot4 == player:
                return True
    return False


def human_turn(player):

    human_nan = True

    while human_nan:
        human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1

        if human_move >= 0 and human_move < 7:
            human_nan = False
        else:
            print("Not a valid move.")

    while not place_token(board_phase_count, human_move, player):
        print_board(board_phase_count)
        print("This column is full choose another column")
        human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1


def drop_piece(board, board_phase, row, col, piece):  # updated to use numpy/board_phase
    board[board_phase, col, row] = piece


def is_valid_location(board, board_phase, col):  # updated to use numpy
    return board[board_phase, col, rows - 1] == 0


def get_next_open_row(board, board_phase, col):  # updated to use board_phase
    for r in range(rows):
        if board[board_phase, col, r] == 0:
            return r


def get_valid_locations(board, board_phase):  # updated to use numpy
    valid_locations = []
    for col in range(cols):
        if is_valid_location(board, board_phase, col):
            valid_locations.append(col)
    return valid_locations


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, board_phase, piece):  # updated for board_phase
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[board_phase, cols // 2, :])]
    center_count = center_array.count(piece)
    score += center_count * 3

    print(center_array)
    # Score Horizontal
    for r in range(rows):
        row_array = [int(i) for i in list(board[board_phase, :, r])]
        for c in range(cols - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(cols):
        col_array = [int(i) for i in list(board[board_phase, c, :])]
        for r in range(rows - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[board_phase, c + i, r + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[board_phase, c + 1, r + 3 - i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board, board_phase):
    return checkWin(board, board_phase, PLAYER_PIECE) or checkWin(board, board_phase, AI_PIECE) or \
            len(get_valid_locations(board, board_phase)) == 0  # could be a problem this line was connected


def minimax(board, board_phase, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board, board_phase)  # U NP
    is_terminal = is_terminal_node(board, board_phase)  # U NP
    if depth == 0 or is_terminal:
        if is_terminal:
            if checkWin(board, board_phase, AI_PIECE):  # changed to use checkWin and not original function
                return None, 100000000000000
            elif checkWin(board, board_phase, PLAYER_PIECE):  # changed to use checkWin and not original function
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, board_phase, AI_PIECE)  # U NP
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, board_phase, col)
            b_copy = board.copy()
            drop_piece(b_copy, board_phase, row, col, AI_PIECE)
            # place_token(b_copy, board_phase, row, col, AI_PIECE)
            new_score = minimax(b_copy, board_phase, depth - 1, alpha, beta, False)[1]
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
            row = get_next_open_row(board, board_phase, col)
            b_copy = board.copy()
            drop_piece(b_copy, board_phase, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, board_phase, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def ai_turn(board, board_phase):
    col, minimax_score = minimax(board, board_phase, 5, -math.inf, math.inf, True)

    if is_valid_location(board, board_phase, col):
        row = get_next_open_row(board, board_phase, col)
        # drop_piece(board,board_phase, row, col, AI_PIECE)
        place_token(board_phase, col, AI_PIECE)


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

    ai_players = True  # bool(int(input("Enter One or Zero for number of AI players.\n")))
    current_player = np.random.randint(1, 3)
    if ai_players:
        while not game_loop:
            if current_player == 1:
                human_turn(current_player)
            else:
                ai_turn(board_list_np, board_phase_count)

            game_loop = checkWin(board_list_np, board_phase_count, current_player)
            current_player = switch_player(current_player, game_loop)
            board_phase_count += 1

    else:
        while not game_loop:
            human_turn(current_player)
            game_loop = checkWin(board_list_np, board_phase_count, current_player)
            current_player = switch_player(current_player, game_loop)
            board_phase_count += 1

    print_board(board_phase_count)
