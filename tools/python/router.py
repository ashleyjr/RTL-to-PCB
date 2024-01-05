import numpy as np


class Copper:

    def __init__(self, size, vert_n_horz):
        self.size = size
        self.vert_n_horz = vert_n_horz
        self.grid = np.zeros((size, size), dtype=int)

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

    def print(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.grid[x][y],end='')
            print()




top = Copper(50, True)
top.print()
print(top.isConnected(1,1,1,3))
top.connect(1,1,1,3)
top.print()
print(top.isConnected(1,1,1,3))
top.connect(8,4,8,19)
top.addKeepOut(20,20,30,30)
top.print()
print(top.isConnected(8,4,8,19))
top.connect(25,0,25,19)
