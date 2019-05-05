import numpy as np
cols = 7
rows = 6
board_size = cols * rows

board_list_np = np.zeros(shape=(board_size, cols, rows),dtype=int)

if __name__ == "__main__":

    print(board_list_np[0, 2, 3])
    print(board_list_np[0, 2, 2])
