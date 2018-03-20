# MazeGenerator
Python script recursively generating perfect mazes. 

### How to use it?

It's pretty simple - all settings needed for the script to run are in mazeGenerator.py. 

You initialize the board by mC.Board(X, Y, Z), where:

X - size of tile 

Y - size of maze 

Z - freeze time between frames


PrintMaze and printMazeSmallStack are board's methods for printing the maze (duuh), 
but in the first case printing is more graphic, you can trace full route of the leading tile.

In the second case algorithm is optimized - it omits some specific cases while adding to stack
therefore making printing faster. 

Feel free to use it, edit it and have fun with it!
