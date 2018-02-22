
from tkinter import *
import random
import sys

sys.setrecursionlimit(10000)
random.seed(9000)

class Cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]  # top right bottom left
        self.visited = False
        self.neighbours = []

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


class Board:
    def __init__(self, sizeOfTile, sizeOfMaze, timeMs):
        self.sizeOfTile = sizeOfTile
        self.sizeOfMaze = sizeOfMaze
        self.time_ms = timeMs
        self.stack = Stack()  # visited tiles will be pushed onto this stack
        self.grid = []  # tile matrix
        self.board = Tk()
        self.board.title("Maze Generator using DFS and Backtracking")
        self.canvas = Canvas(self.board, width=self.sizeOfMaze, height=self.sizeOfMaze, bg="gray")  # creates Canvas
        self.canvas.create_text(self.sizeOfMaze-60, self.sizeOfMaze-10, font="Arial 10", text="Created by FH")
        self.canvas.pack()
        self.rows = int(int(self.canvas.cget('height'))/self.sizeOfTile)
        self.cols = int(int(self.canvas.cget('width'))/self.sizeOfTile)
        self.stack = Stack()  # visited tiles will be on this stack
        for i in range(self.rows):  # creates array (1d grid) of Cells
            for j in range(self.cols):
                cell = Cell(i, j)
                self.grid.append(cell)

        for i in self.grid:
            self.checkNeighbours(i)  # goes through all tiles, fills neighbours array in each

    def index(self, i, j):  # returns 1D index for 2D pseudomatrix
        if i < 0 or j < 0 or i > self.rows-1 or j > self.cols-1:
            return -1
        return self.cols*i+j

    def checkNeighbours(self, cell):
        topIndex = self.index(cell.i-1, cell.j)
        if topIndex > -1:
            cell.neighbours.append(self.grid[topIndex])
        rightIndex = self.index(cell.i, cell.j+1)
        if rightIndex > -1:
            cell.neighbours.append(self.grid[rightIndex])
        bottomIndex = self.index(cell.i+1, cell.j)
        if bottomIndex > -1:
            cell.neighbours.append(self.grid[bottomIndex])
        leftIndex = self.index(cell.i, cell.j-1)
        if leftIndex > -1:
            cell.neighbours.append(self.grid[leftIndex])

    def show(self, cell):
        x = cell.j*self.sizeOfTile  # x position for the top left corner
        y = cell.i*self.sizeOfTile  # y position for the top left corner
        if cell.visited:
            self.canvas.create_rectangle(x, y, x+self.sizeOfTile, y+self.sizeOfTile, fill='#5D33FF', width=0)
        if cell.walls[0]:
            self.canvas.create_line(x, y, x+self.sizeOfTile, y)
        if cell.walls[1]:
            self.canvas.create_line(x+self.sizeOfTile, y, x+self.sizeOfTile, y+self.sizeOfTile)
        if cell.walls[2]:
            self.canvas.create_line(x+self.sizeOfTile, y+self.sizeOfTile, x, y+self.sizeOfTile)
        if cell.walls[3]:
            self.canvas.create_line(x, y+self.sizeOfTile, x, y)
            self.canvas.after(self.time_ms)
        self.canvas.update()

    def leadTile(self, cell):
        x = cell.j * self.sizeOfTile
        y = cell.i * self.sizeOfTile
        self.canvas.create_rectangle(x, y, x+self.sizeOfTile, y+self.sizeOfTile, fill='#FF0000', width=0)
        self.canvas.update()

    def deleteWall(self, current, next):
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
        self.canvas.update()

    def printMaze(self, current):
        current.visited = True
        nextTile = current.randomNeighbour()
        if nextTile != -1:  # if nextTile exists
            self.stack.push(current)  # push to stack
            self.deleteWall(current, nextTile)
            self.leadTile(current)  # print leadTile
            self.show(current)
            self.printMaze(nextTile)  # recursively go to the next tile
        elif not self.stack.isEmpty():  # if stack is not empty
            self.leadTile(current)
            self.show(current)
            self.printMaze(self.stack.pop())  # go back to the last tile
        else:
            print("Maze done!")
            return 0

    def printMazeSmallStack(self, current):  # doesn't push to stack if no nbs after the last one
        current.visited = True
        nextTile = current.randomNeighbour()
        if nextTile != -1:  # if nextTile exists
            nextTile.visited = True
            for i in current.neighbours:
                if not i.visited:
                    self.stack.push(current)  # push to stack
                    break
            self.deleteWall(current, nextTile)
            self.leadTile(current)  # print leadTile
            self.show(current)
            self.printMazeSmallStack(nextTile)  # recursively go to the next tile
        elif not self.stack.isEmpty():  # if stack is not empty
            self.leadTile(current)
            self.show(current)
            self.printMazeSmallStack(self.stack.pop())  # go back to the last tile
        else:
            print("Maze done!")
            return 0


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
