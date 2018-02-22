'''
Recursive Maze Generator
Author: Filip Hein
12.02.2018
'''


import mazeClass as mC
import time

board = mC.Board(20, 600, 10)
currentTile = board.grid[0]  # picks the tile we start from
start_time = time.time()
#  board.printMaze(currentTile)  # the fun part!
board.printMazeSmallStack(currentTile)  # the fun part!
print("{} seconds".format(time.time()-start_time))
board.canvas.mainloop()
