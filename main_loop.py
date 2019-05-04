
cols = 7
rows = 6
board_size = cols * rows
board_list = [None] * ((cols * rows)*(board_size))

current_turn = 2
current_col = 6
current_row = 0


current_index = (current_turn * board_size) + (current_col * 6) + (current_row)




if __name__ == "__main__":

    print(len(board_list))
    print(current_index)
