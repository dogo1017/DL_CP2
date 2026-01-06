board = [[]]

board_size_x = int(input("How long do you want the x-axis of board to be: "))
board_size_y = int(input("How long do you want the y-axis of board to be: "))

for i in range(board_size_x):
    board[0].append(1)

for i in range(board_size_y-2):
    board.append([])
    board[i].append(1)
    for j in range(board_size_x-2):
        board[i].append(0)
    board[i].append(1)

for i in range(len(board)):
    for j in range(len(board[i])):
        print(board[i][j], "", end = '')
    print("")

snake_trail = []