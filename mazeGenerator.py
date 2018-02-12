'''
Recursive Maze Generator
Author: Filip Hein
12.02.2018
'''


from tkinter import *
import random
import sys
import time


sys.setrecursionlimit(10000)
global stack
sizeOfTile = 30
sizeOfMaze = 600  # value x value canvas size
grid = []  # tile matrix
time_ms = 30  # refresh time


def index(i, j):  # returns 1D index for 2D pseudomatrix
    if i < 0 or j < 0 or i > rows-1 or j > cols-1:
        return -1
    return cols*i+j


def deleteWall(current, next):
    if current.i - next.i == 1:  # if upper neighbour
        current.walls[0] = False
        next.walls[2] = False
    elif current.i - next.i == -1:  # lower nb
        current.walls[2] = False
        next.walls[0] = False
    if current.j - next.j == 1:  # left nb
        current.walls[3] = False
        next.walls[1] = False
    elif current.j - next.j == -1:  # right nb
        current.walls[1] = False
        next.walls[3] = False
    c.update()


def printMaze(current):
    current.visited = True
    nextTile = current.randomNeighbour()
    if nextTile != -1:  # if nextTile exists
        stack.push(current)  # push to stack
        deleteWall(current, nextTile)
        current.leadTile()  # print leadTile
        current.show()
        printMaze(nextTile)  # recursively go to the next tile
    elif not stack.isEmpty():  # if stack is not empty
        current.leadTile()
        current.show()
        printMaze(stack.pop())  # go back to the last tile
    else:
        print("Maze done!")
        return 0


def printMazeSmallStack(current):  # doesn't push to stack if no nbs after the last one
    current.visited = True
    nextTile = current.randomNeighbour()
    if nextTile != -1:  # if nextTile exists
        nextTile.visited = True
        for i in current.neighbours:
            if not i.visited:
                stack.push(current)  # push to stack
                break
        deleteWall(current, nextTile)
        current.leadTile()  # print leadTile
        current.show()
        printMazeSmallStack(nextTile)  # recursively go to the next tile
    elif not stack.isEmpty():  # if stack is not empty
        current.leadTile()
        current.show()
        printMazeSmallStack(stack.pop())  # go back to the last tile
    else:
        print("Maze done!")
        return 0


class Cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]  # top right bottom left
        self.visited = False
        self.neighbours = []

    def show(self):
        x = self.j*sizeOfTile  # x position for the top left corner
        y = self.i*sizeOfTile  # y position for the top left corner
        if self.visited:
            c.create_rectangle(x, y, x+sizeOfTile, y+sizeOfTile, fill='#5D33FF', width=0)
        if self.walls[0]:
            c.create_line(x, y, x+sizeOfTile, y)
        if self.walls[1]:
            c.create_line(x+sizeOfTile, y, x+sizeOfTile, y+sizeOfTile)
        if self.walls[2]:
            c.create_line(x+sizeOfTile, y+sizeOfTile, x, y+sizeOfTile)
        if self.walls[3]:
            c.create_line(x, y+sizeOfTile, x, y)
        c.after(time_ms)
        c.update()

    def leadTile(self):
        x = self.j * sizeOfTile
        y = self.i * sizeOfTile
        c.create_rectangle(x, y, x+sizeOfTile, y+sizeOfTile, fill='#FF0000', width=0)
        c.update()

    def checkNeighbours(self):
        topIndex = index(self.i-1, self.j)
        if topIndex > -1:
            self.neighbours.append(grid[topIndex])
        rightIndex = index(self.i, self.j+1)
        if rightIndex > -1:
            self.neighbours.append(grid[rightIndex])
        bottomIndex = index(self.i+1, self.j)
        if bottomIndex > -1:
            self.neighbours.append(grid[bottomIndex])
        leftIndex = index(self.i, self.j-1)
        if leftIndex > -1:
            self.neighbours.append(grid[leftIndex])

    def randomNeighbour(self):
        if self.areAvailableNeighbours():
            r = random.randint(0, len(self.neighbours)-1)  # pick random neighbour
            while self.neighbours[r].visited:  # pick randomly until it's not visited
                r = random.randint(0, len(self.neighbours)-1)
            return self.neighbours[r]  # return randomly picked neighbour
        else:
            return -1

    def areAvailableNeighbours(self):
        for i in self.neighbours:
            if not i.visited:
                return True
            if i.visited:
                continue
        return False


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


board = Tk()
board.title("Maze Generator using DFS and Backtracking")
c = Canvas(board, width=sizeOfMaze, height=sizeOfMaze, bg="gray")  # creates Canvas
c.create_text(sizeOfMaze-60, sizeOfMaze-10, font="Arial 10", text="Created by FH")
c.pack()
stack = Stack()  # visited tiles will be on this stack

rows = int(int(c.cget('height'))/sizeOfTile)
cols = int(int(c.cget('width'))/sizeOfTile)

for i in range(rows):  # creates array (1d grid) of Cells
    for j in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

for i in grid:
    i.checkNeighbours()  # goes through all tiles, fills neighbours array in each

currentTile = grid[0]  # picks the tile we start from
start_time = time.time()

# printMaze(currentTile)  # the fun part!
printMazeSmallStack(currentTile)  # the fun part!
print("{} seconds".format(time.time()-start_time))
c.mainloop()
