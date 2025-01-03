import numpy as np

win = np.zeros((192,10,10),int)

for i in range(0, 6):
    for j in range(0, 10):
        for k in range(0, 5):
                win[j+(i*10), j, k+i] = 5
for i in range(0, 6):
    for j in range(0, 10):
        for k in range(0, 5):
                win[60+j+(i*10),  k+i, j] = 5  
for i  in range(0, 6):
    for j in range(0, 6):
        for k in range(0, 5):
            win[120+j+(i*6), k+i, k+j] = 5 
for i  in range(0, 6):
    for j in range(0, 6):
        for k in range(0, 5):        
            win[152+j+i*6, k+j, 4-k+i] = 5      
# print(win)

def WeightComputing(PlayerBoard, PlayerWinCount):
    weight = np.zeros((10, 10),int)
    for i in range(0,192):
        if PlayerWinCount[i] < 50:
            for j in range (0, 10):
                for k in range(0, 10):
                    weight[j,k] += (win[i,j,k]  * PlayerBoard[j,k] )
        if 3 <= PlayerWinCount[i] :
            for j in range (0, 10):
                for k in range(0, 10):
                    weight[j,k] += (win[i,j,k]  * PlayerBoard[j,k]  *3)



    # print(weight)
    return np.argmax(weight)


board = np.zeros((10,10),int)
AIBoard = [np.ones((10,10),int),np.ones((10,10),int)]
CurrentPlayer = 1
Next = 1
WinCount = np.zeros((2,192),int)
IsLooping = True

while IsLooping:
    index = WeightComputing(AIBoard[CurrentPlayer], WinCount[CurrentPlayer, :])
#   print(index)
    x = int(index / 10)
    y = index % 10
    board[x,y] = CurrentPlayer + 1
    if board[x,y] == 1:
        print(f'P1: x:{y}, y:{x}')
    if board[x,y] == 2:
        print(f'P2: x:{y}, y:{x}')
    for j in range(0, 192):
        if win[j,x,y] > 0:
            WinCount[CurrentPlayer, j] += 1
            WinCount[CurrentPlayer + Next * -1, j] = 50
        if WinCount[CurrentPlayer, j] == 5:
            IsLooping = False
            if board[x,y] == 1:
                print(f'P1 win')
            if board[x,y] == 2:
                print(f'P2 win')
            break

    # print(WinCount)
    AIBoard[CurrentPlayer][x,y] = 0 #1
    Next *= -1
    CurrentPlayer += Next
    AIBoard[CurrentPlayer][x,y] = -1 #2
    # print(AIBoard)
    print(board)



