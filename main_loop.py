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

    human_nan = True

    while human_nan:
        human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1

        if human_move > 0 and human_move < 7:
            human_nan = False

    while not place_token(board_phase_count, human_move, player):
        print_board(board_phase_count)
        print("This column is full choose another column")
        human_move = int(input("Player: {} Enter number 1 to 7 \n".format(player))) - 1


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r

        def winning_move(board, piece):
            # Check horizontal locations for win
            for c in range(cols - 3):
                for r in range(rows):
                    if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                        c + 3] == piece:
                        return True

            # Check vertical locations for win
            for c in range(cols):
                for r in range(rows - 3):
                    if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                        c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(cols - 3):
                for r in range(rows - 3):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                            board[r + 3][
                                c + 3] == piece:
                        return True

            # Check negatively sloped diaganols
            for c in range(cols - 3):
                for r in range(3, rows):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                            board[r - 3][
                                c + 3] == piece:
                        return True

def get_valid_locations(board):
    valid_locations = []
    for col in range(cols):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(cols - 3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(cols - 3):
        for r in range(rows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(cols - 3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

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

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, cols // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(cols - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(cols):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

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

    ai_players = True  # bool(int(input("Enter One or Zero for number of AI players.\n")))
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
