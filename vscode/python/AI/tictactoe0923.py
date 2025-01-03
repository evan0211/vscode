import numpy as np

win = np.zeros((8,3,3),int)
for i in range(0, 3):
  win[i, i, 0] = 5
  win[i, i, 1] = 5
  win[i, i, 2] = 5

  win[i+3, 0, i] = 5
  win[i+3, 1, i] = 5
  win[i+3, 2, i] = 5

  win[6, i, i] = 5
  win[7, 2-i, i] = 5
#print(win)

def WeightComputing(PlayerBoard, PlayerWinCount):
  weight = np.zeros((3,3),int)
  for i in range(0,8):
    if PlayerWinCount[i] < 5:
      for j in range (0,3):
        for k in range(0,3):
          weight[j,k] += win[i,j,k] * PlayerBoard[j,k]
  #print(weight)
  return np.argmax(weight)

board = np.zeros((3,3),int)
AIBoard = [np.ones((3,3),int),np.ones((3,3),int)]
CurrentPlayer = 1
Next = 1
WinCount = np.zeros((2,8),int)
IsLooping = True
while IsLooping:
  index = WeightComputing(AIBoard[CurrentPlayer], WinCount[CurrentPlayer, :])
  x = int(index / 3)
  y = index % 3
  print(f'x:{x}, y:{y}')
  board[x,y] = CurrentPlayer + 1
  for j in range(0,8):
    if win[j,x,y] > 0:
      WinCount[CurrentPlayer, j] += 1
      WinCount[CurrentPlayer + Next * -1, j] = 5
      if WinCount[CurrentPlayer, j] == 3:
        IsLooping = False
        break

  print(WinCount)
  AIBoard[CurrentPlayer][x,y] = 0
  Next *= -1
  CurrentPlayer += Next
  AIBoard[CurrentPlayer][x,y] = -1
  # print(AIBoard)
  print(board)