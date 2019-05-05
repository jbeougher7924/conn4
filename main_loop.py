import numpy as np
cols = 7
rows = 6
board_size = cols * rows

token_used_cols_np = np.full(shape=(cols), fill_value=(6), dtype=int)

board_list_np = np.zeros(shape=(board_size, cols, rows),dtype=int)


def place_token(board_phase, column):

    if token_used_cols_np[column] >= 0:
        token_used_cols_np[column] -= 1
        return True
    else:
        return False





if __name__ == "__main__":

    # print(board_list_np[0, 2, 3])
    # print(board_list_np[0, 2, 2])
    tempCols = 3;
    token_used_cols_np[tempCols] = -1
    while place_token(1, tempCols) == False:
        print(token_used_cols_np)
        tempCols = np.random.randint(7)

    print(token_used_cols_np)