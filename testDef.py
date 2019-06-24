import numpy as np


ROW_COUNT = 6
COLUMN_COUNT = 7

game_rows = rows = ROW_COUNT
game_cols = cols = COLUMN_COUNT

# myList = np.array([0] * (rows * cols)).reshape(rows, cols)

# myList = np.random.randint(low=-1, high=2, size=(rows*cols)).reshape(rows,cols)
myList = np.random.randint(low=0, high=1, size=(rows*cols)).reshape(rows,cols)

# print(myList)


# def mod_list(myList):
#
#     for row in myList:
#         randnum = np.random.randint(low=0, high=8, size=1)
#         print(randnum[0])
#         for i in range(0,randnum[0]):
#             row[i] = 1
#
#     return myList


def mod_list(myList):
    randnum = np.random.randint(low=0, high=6, size=(6, 2))
    print(randnum)
    count = 0
    for pos in randnum:

        for i in range(pos[0], -1, -1):
            myList[i, pos[1]] = 1

    for row in myList:
        pass
        # print(randnum)
        # myList[randnum[0], randnum[1]] = 1




    return myList

def check_action(myList):

    one_above_all = False

    # for row in myList:
    #     # print(row)
    #     firstOne = False
    #     for i in range(6, -1, -1):
    #
    #         if firstOne:
    #             if row[i] == 0:
    #                 one_above_all = True
    #
    #         if row[i] != 0:
    #             firstOne = True
    #
    #     print(one_above_all)
    #     print(row)
    #     one_above_all = False

    for i in range(cols):

        first_zero = False
        for j in range(rows):
            if myList[j, i] != 0:
                if first_zero:
                    if myList[j, i] != 0:
                        one_above_all = True
            else:
                first_zero = True

        # print(one_above_all)
        # one_above_all = False
    return one_above_all


def top_zero(myList):
    ## create a copy of the board which is linear
    temp_copy = np.array(np.copy(myList).reshape(-1))

    ## fetch all the indexes that are free or zero so those can used for playing next move
    zero_indexes = []
    for row in myList:
        # print(row)
        firstOne = False
        for i in range(6, -1, -1):
            pass


    for index, item in enumerate(temp_copy):
        if item == 0:
            zero_indexes.append(index)
    return zero_indexes


def top_zero2(myList):

    ## fetch all the indexes that are free or zero so those can used for playing next move
    zero_indexes = []
    # for index, row in enumerate(myList):
    #     print(index)
    #     lowestZero = -1
    #     for i in range(6, -1, -1):
    #         if row[i] == 0:
    #             lowestZero = i
    #         else:
    #             break
    #     zero_indexes.append(index * 7 + lowestZero)

    for i in range(cols):
        for j in range(rows):
            if myList[j, i] == 0:
                zero_indexes.append(j * 7 + i)
                break

    return zero_indexes


# check_action(myList)


print(mod_list(myList))
print(check_action(myList))


# zero_indexes = top_zero(myList)
zero_indexes2 = top_zero2(myList)
#
# print(zero_indexes)
print(zero_indexes2)
