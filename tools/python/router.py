import numpy as np
import random

class Grid:

    def __init__(self, size):
        self.size = size
        self.grid = np.ones((size, size), dtype=int)
        self.last_grid = self.grid

    def print(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.grid[x][y],end='')
            print()

    def addKeepOut(self, x0, y0, x1, y1):
        ''' Add a box keepout region '''
        if x0 < x1:
            xs = x0
            xe = x1
        else:
            xs = x1
            xe = x0
        if y0 < y1:
            ys = y0
            ye = y1
        else:
            ys = y1
            ye = y0
        for x in range(xs,xe+1):
            for y in range(ys, ye+1):
                self.grid[x][y] = 2

    def isKeepOut(self, x, y):
        return self.grid[x][y] == 2

    def permutate(self, n):
        self.last_grid = np.copy(self.grid)
        for _ in range(n):
            # TODO: This could be better by
            # removing keepouts from random list
            while(True):
                x = random.randrange(self.size)
                y = random.randrange(self.size)
                if not self.isKeepOut(x,y):
                    break
            self.grid[x][y] = 0

    def undoPermutate(self):
        self.grid = self.last_grid

    def remove(self, x, y):
        if not self.isKeepOut(x, y):
            self.grid[x][y] = 0

    def add(self, x, y):
        if not self.isKeepOut(x, y):
            self.grid[x][y] = 1

    def isPresent(self, x, y):
        return self.grid[x][y] == 1


class Copper(Grid):

    def __init__(self, size, vert_n_horz):
        super().__init__(size)
        self.vert_n_horz = vert_n_horz

    def isConnected(self, x0, y0, x1, y1):
        assert x0 < self.size
        assert x1 < self.size
        assert y0 < self.size
        assert y1 < self.size
        # Rotate if required
        if self.vert_n_horz:
            a0 = x0
            a1 = x1
            b0 = y0
            b1 = y1
        else:
            a0 = y0
            a1 = y1
            b0 = x0
            b1 = x1
        # Return if not on same line
        if a0 != a1:
            return False
        # Find the lower one to start
        if b0 < b1:
            s = b0
            e = b1
        else:
            s = b1
            e = b0
        # Walk along line
        for i in range(s,e+1):
            if self.vert_n_horz:
                if self.grid[i][a0] != 1:
                    return False
            else:
                if self.grid[a0][i] != 1:
                    return False
        return True

    def canConnect(self, x0, y0, x1, y1):
        # Rotate if required
        if self.vert_n_horz:
            a0 = x0
            a1 = x1
            b0 = y0
            b1 = y1
        else:
            a0 = y0
            a1 = y1
            b0 = x0
            b1 = x1
        # Fail if not on same line
        if a0 != a1:
            return False
        # Find the lower one to start
        if b0 < b1:
            s = b0
            e = b1
        else:
            s = b1
            e = b0
        # Walk along line
        for i in range(s,e+1):
            if self.vert_n_horz:
                if self.grid[i][a0] == 2:
                    return False
            else:
                if self.grid[a0][i] == 2:
                    return False
        return True

    def connect(self, x0, y0, x1, y1):
        assert self.canConnect(x0, y0, x1, y1)
        # Rotate if required
        if self.vert_n_horz:
            a0 = x0
            a1 = x1
            b0 = y0
            b1 = y1
        else:
            a0 = y0
            a1 = y1
            b0 = x0
            b1 = x1
        # Fail if not on same line
        assert a0 == a1
        # Find the lower one to start
        if b0 < b1:
            s = b0
            e = b1
        else:
            s = b1
            e = b0
        # Walk along line
        for i in range(s,e+1):
            if self.vert_n_horz:
                self.grid[i][a0] = 1
            else:
                self.grid[a0][i] = 1

class Pcb:

    def __init__(self,size):
        self.size = size
        self.top = Copper(size, False)
        self.bottom = Copper(size, True)
        self.vias = Grid(size)

    def isConnected(self, x0, y0, x1, y1):
        '''
        Check if two points are connected.
        Start and ends on the top layer,
        Even hopcounts == top
        Odd hopcount == bottom
        '''
        to_pop = 1
        stack = [(x0,y0)]
        for hopcount in range(5):
            #print(hopcount)
            for _ in range(to_pop):
                x,y = stack.pop()
                for i in range(self.size):
                    for j in range(self.size):
                        if (x,y) != (i,j):
                            # TODO: Vias indexing appears the wrong way round
                            if (hopcount % 2) == 0:
                                if self.top.isConnected(x,y,i,j):
                                    if (i,j) == (x1,y1):
                                        return True
                                    if self.vias.isPresent(j,i):
                                        stack.insert(0, (i,j))
                            else:
                                if self.bottom.isConnected(x,y,i,j) and self.vias.isPresent(j,i):
                                    stack.insert(0, (i,j))
            #print(stack)
            to_pop = len(stack)
            #print(to_pop)
        return False

    def print(self):
        print("Top:")
        self.top.print()
        print("Vias:")
        self.vias.print()
        print("Bottom:")
        self.bottom.print()

    def permutate(self, n):
        self.top.permutate(n)
        self.vias.permutate(n)
        self.bottom.permutate(n)

    def undoPermutate(self, n):
        self.top.undoPermutate()
        self.vias.undoPermutate()
        self.bottom.undoPermutate()


top = Copper(20, True)
#top.connect(1,1,1,3)
#top.connect(8,4,8,19)
#top.addKeepOut(5,5,15,15)
#top.connect(25,0,25,19)
#top.permutate(1)




nets = [
    (1,1,18,18),
    (19,1,19,8)
]

avoids = [
    (1,1,19,8),
    (1,1,19,8)
]

print("")
pcb = Pcb(20)
for i in range(10000):
    print(f"\r{i}",end='')
    pcb.permutate(1)
    u = False
    for x0,y0,x1,y1 in nets:
        if not pcb.isConnected(x0,y0,x1,y1):
            u = True

    if u:
        pcb.undoPermutate(1)

print("")
pcb.print()

#top.print()
#for _ in range(2000):
#    top.permutate(1)
#    if not top.isConnected(1,2,1,17):
#        top.undoPermutate()
#
#top.print()
