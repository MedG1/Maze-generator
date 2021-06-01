import numpy as np
import matplotlib.pyplot as plt
from random import choice

class Stack:
    def __init__(self, ls = None):
        if ls is None:
            self.ls = []
        else:
            self.ls = ls

    def push(self, item):
        self.ls.append(item)
    
    def pop(self):
        assert self.ls != []
        self.ls.pop()

    def top(self):
        assert self.ls != []
        return self.ls[-1]

class Maze:
   
    def __init__(self, size):
        assert len(size) == 2 and all(i >= 2 for i in size), 'Maze is a 2 dimentional object'
        y, x = size
        self.h = y
        self.w = x
        self.arr = np.zeros((2 * y - 1, 2 * x - 1), dtype = np.bool)
        self.done = np.zeros(size, dtype = np.bool)
       
    def get_neighbours(self, cell):
        y, x = cell[0], cell[1]
        e = {(-2, 0), (0, -2), (0, 2), (2,0)}
        res = []
        for i, j in e:
            if 2 * self.h -1 > y + i >= 0 and 2 * self.w - 1> x + j >= 0:
                if not(self.arr[y + i, x + j]):
                    res.append((y + i, x + j))
        return res
   
    def break_wall(self, cell1, cell2):
        y1, x1 = cell1
        y2, x2 = cell2
        if y1 == y2 and abs(x1 - x2) == 2:
            ywall = y1
            xwall = max(x1, x2) - 1
        elif x1 == x2 and abs(y1 - y2) == 2:
            ywall = max(y1, y2) - 1
            xwall = x1
        else:
            raise ValueError('cell1 and cell2 are not neighbours')
        self.arr[ywall, xwall] = True
       
    def set_start(self, coord):
        y, x = coord
        self.arr[y, x] = True
        return coord

    # generating a maze using recursion severely limites the size of mazes because of the recursion depth limit
    def generate_recursive(self, start, traversed):
        if np.all(self.done):
            print('done (with recursion) :)')
        else:
            traversed.push(start)
            y, x = start
            self.arr[y, x] = self.done[y//2, x//2] = True
            neighbours = self.get_neighbours(start)
            #print(f'currently on {start}, neighbours: {neighbours}')
            if neighbours != []:
                new = choice(neighbours)
                i, j = new
                self.arr[i, j] = self.done[i//2, j//2] = True
                #print('advancing: from ', start, ' to ', new)
                self.break_wall(start, new)
                self.generate_recursive(new, traversed)
            else:
                while neighbours == []:
                    traversed.pop()
                    new = traversed.top()
                    neighbours = self.get_neighbours(new)
                    #print(f'backtracking to {new}, availble neighbours: {neighbours}')
                self.generate_recursive(new, traversed)
        print('done (maze generated using recursion) :)')
               
    def generate(self, start):
        traversed = Stack()
        while not(np.all(self.done)):
            traversed.push(start)
            y, x = start
            self.arr[y, x] = self.done[y//2, x//2] = True
            neighbours = self.get_neighbours(start)
            #print(f'currently on {i}, neighbours: {neighbours}')
            if neighbours != []:
                new = choice(neighbours)
                i, j = new
                self.arr[i, j] = self.done[i//2, j//2] = True
                #print('advancing: from ', start, ' to ', new)
                self.break_wall(start, new)
                start = new
            else:
                while neighbours == []:
                    traversed.pop()
                    new = traversed.top()
                    neighbours = self.get_neighbours(new)
                    #print(f'backtracking to {new}, availble neighbours: {neighbours}')
                start = new
        print('done (maze generated using while loop) :)')
           
               
    def display(self):
        y, x = self.arr.shape
        frame = np.zeros((y + 2, x + 2), dtype = np.bool)
        frame[1:y + 1, 1:x + 1] = True
        frame[frame] = self.arr[np.ones(self.arr.shape, dtype = np.bool)]
        frame[1, 0] = True
        frame[y + 1 ,x] = True
        plt.imshow(frame, cmap = 'gray')
        plt.show()
       # return frame

m = Maze((50, 20))
m.generate((0, 0))
m.display()
