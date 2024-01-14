import numpy as np
import random
import os
import math

class Grid:

    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.last_grid = self.grid

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
        #assert x0 < self.size
        #assert x1 < self.size
        #assert y0 < self.size
        #assert y1 < self.size
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
            return 0
        # Find the lower one to start
        if b0 < b1:
            s = b0
            e = b1
        else:
            s = b1
            e = b0
        # Take slice of line
        if self.vert_n_horz:
            return (min(self.grid[a0,s:e+1]) == 1)
        return (min(self.grid[s:e+1,a0]) == 1)


    def lenConnected(self, x0, y0, x1, y1):
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
            return 0
        # Find the lower one to start
        if b0 < b1:
            s = b0
            e = b1
        else:
            s = b1
            e = b0
        # Walk along line
        length = 0
        for i in range(s,e+1):
            if self.vert_n_horz:
                if self.grid[a0][i] != 1:
                    return 0
            else:
                if self.grid[i][a0] != 1:
                    return 0
            length += 1
        return length

    def __update(self, x, y, v):
        if self.grid[x][y] !=2:
            self.grid[x][y] = v

    def remove(self, x, y):
        self.__update(x ,y, 0)

    def add(self, x, y):
        self.__update(x, y, 1)

    def isPresent(self, x, y):
        return self.grid[x][y] == 1



class Pcb:

    def __init__(self, size, fanouts):
        self.size = size
        self.top = Copper(size, False)
        self.bottom = Copper(size, True)
        self.vias = Grid(size)
        self.fanouts = fanouts
        self.nets = []
        # Add all nets required
        for sx,sy in fanouts:
            for ex,ey in fanouts[(sx,sy)]:
                self.nets.append((sx,sy,ex,ey))
        # Add all cross connects
        self.crosses = []
        for sx,sy in self.fanouts:
            for ex,ey in self.fanouts:
                if (sx,sy) != (ex,ey):
                    # Sources to sources
                    if (ex,ey,sx,sy) not in self.crosses:
                        self.crosses.append((sx,sy,ex,ey))
                    # Sources to sinks
                    for x,y in self.fanouts[(ex,ey)]:
                        if (ex,ey,sx,sy) not in self.crosses:
                            self.crosses.append((sx,sy,x,y))
        #self.addStartEnds()

    def listNets(self):
        return self.nets

    def distance(self,x0,y0,x1,y1):
        x = abs(x0 - x1)
        y = abs(y0 - y1)
        return x + y

    def search(self):
        num_nets = len(self.nets)
        for n_i,n in enumerate(self.nets):

            top_n_bottom = True
            sx,sy,ex,ey = n
            x = sx
            y = sy
            avoids = []
            self.top.add(x,y)
            # Timeout
            for move in range(self.size * 2):
                # Done
                if ((x,y) == (ex,ey)) and top_n_bottom:
                    break

                # Print Routing update
                os.system('clear')
                self.print()
                print(f"\rNet: {n_i}/{num_nets},{sx},{ey},{ex},{ey},{x},{y},{top_n_bottom},{move},{avoids}",end='')

                # Find possible next steps
                tpos = []
                bpos = []
                if top_n_bottom:
                    if  not self.bottom.isKeepOut(x,y) and \
                        not self.vias.isKeepOut(x,y) and \
                        not (x,y) in avoids:
                        bpos.append((x,y))
                    if x != 0:
                        if  not self.top.isKeepOut(x-1,y) and \
                            not (x-1,y) in avoids:
                            tpos.append((x-1,y))
                    if x != (self.size-1):
                        if  not self.top.isKeepOut(x+1,y) and \
                            not (x+1,y) in avoids:
                            tpos.append((x+1,y))
                else:
                    if  not self.top.isKeepOut(x,y) and \
                        not self.vias.isKeepOut(x,y) and \
                        not (x,y) in avoids:
                        tpos.append((x,y))
                    if y != 0:
                        if  not self.bottom.isKeepOut(x,y-1) and \
                            not (x,y-1) in avoids:
                            bpos.append((x,y-1))
                    if y != (self.size-1):
                        if  not self.bottom.isKeepOut(x,y+1) and \
                            not (x,y+1) in avoids:
                            bpos.append((x,y+1))

                # Nowhere to go
                assert (len(bpos) + len(tpos)) > 0

                # Find the distances of all points
                tdis = []
                for tx,ty in tpos:
                    tdis.append(self.distance(tx,ty,ex,ey))
                bdis = []
                for bx,by in bpos:
                    bdis.append(self.distance(bx,by,ex,ey))

                # Try shortest distance
                while True:
                    if (len(tdis) == 0) and (len(bdis) == 0):
                        break

                    # Check there is stuff
                    if len(tdis) > 0:
                        tmin = min(tdis)
                    else:
                        tmin = math.inf
                    if len(bdis) > 0:
                        bmin = min(bdis)
                    else:
                        bmin = math.inf


                    # Make the shortest distance
                    if tmin < bmin:
                        i = tdis.index(min(tdis))
                        x,y = tpos[i]

                        t_keep_if_bad = self.top.isPresent(x,y)
                        self.top.add(x,y)

                        if not top_n_bottom:
                            self.vias.add(x,y)

                        if not self.hasCrossConnect():
                            top_n_bottom = True
                            break

                        if not t_keep_if_bad:
                            self.top.remove(x,y)

                        if not top_n_bottom:
                            self.vias.remove(x,y)

                        del tpos[i]
                        del tdis[i]
                        # Avoids this in the future
                        avoids.append((x,y))
                    else:
                        i = bdis.index(min(bdis))
                        x,y = bpos[i]

                        b_keep_if_bad = self.bottom.isPresent(x,y)
                        self.bottom.add(x,y)

                        if top_n_bottom:
                            self.vias.add(x,y)

                        if not self.hasCrossConnect():
                            top_n_bottom = False
                            break

                        if not b_keep_if_bad:
                            self.bottom.remove(x,y)

                        if top_n_bottom:
                            self.vias.remove(x,y)

                        del bpos[i]
                        del bdis[i]
                        # Avoids this in the future
                        avoids.append((x,y))

            os.system('clear')
            self.print()

    def addStartEnds(self):
        # Initialise the top copper with all the start/end points
        for sx,sy,ex,ey in self.nets:
            self.top.add(sx,sy)
            self.top.add(ex,ey)

    def isPresentTop(self,x,y):
        self.top.isPresent(x,y)

    def isPresentVia(self,x,y):
        self.vias.isPresent(x,y)

    def isPresentBottom(self,x,y):
        self.bottom.isPresent(x,y)

    def removeTop(self,x,y):
        self.top.remove(x,y)

    def addTop(self,x,y):
        self.top.add(x,y)

    def removeVia(self,x,y):
        self.vias.remove(x,y)

    def addVia(self,x,y):
        self.vias.add(x,y)

    def removeBottom(self,x,y):
        self.bottom.remove(x,y)

    def addBottom(self,x,y):
        self.bottom.add(x,y)

    def isConnected(self, x0, y0, x1, y1):
        '''
        - Allow hopcount to go through a via on every pos on the PCB
        '''
        if not self.top.isPresent(x1,y1):
            return False
        if not self.top.isPresent(x0,y0):
            return False
        to_pop = 1
        stack = [(x0,y0)]
        for hopcount in range(self.size * self.size):
            end = len(stack)
            start = end - to_pop
            to_pop = 0
            for s in range(start,end):
                x,y = stack[s]
                for i in range(self.size):
                    for j in range(self.size):
                        c = (i,j)
                        if (hopcount % 2) == 0:
                            if self.top.isConnected(x,y,i,j):
                                if c == (x1,y1):
                                    return True
                                if self.vias.isPresent(i,j):
                                    if (c not in stack) or (x,y == c):
                                        stack.append(c)
                                        to_pop += 1
                        else:
                            con = self.bottom.isConnected(x,y,i,j)
                            via = self.vias.isPresent(i,j)
                            if con and via and (c not in stack):
                                stack.append(c)
                                to_pop += 1
            if to_pop == 0:
                return False
        print(f"\n{stack}")
        assert False

    def numNets(self):
        return len(self.nets)

    def numConnected(self):
        num = 0
        for sx,sy,ex,ey in self.nets:
            if self.isConnected(sx,sy,ex,ey):
                num += 1
        return num

    def hasCrossConnect(self):
        l = []
        for sx,sy,ex,ey in self.crosses:
            if self.isConnected(sx,sy,ex,ey):
                return True
        return False

    def numCrossConnected(self):
        return len(self.listCrossConnected())

    def listCrossConnected(self):
        l = []
        for sx,sy,ex,ey in self.crosses:
            if self.isConnected(sx,sy,ex,ey):
                l.append((sx,sy,ex,ey))
        return l

    def listConnected(self):
        checks = []
        l = []
        for sx,sy in self.fanouts:
            for ex,ey in self.fanouts[(sx,sy)]:
                checks.append((sx,sy,ex,ey))
        for sx,sy,ex,ey in checks:
            if self.isConnected(sx,sy,ex,ey):
                l.append((sx,sy,ex,ey))
        return l

    def cleanUp(self):
        n = self.numConnected()
        rms = 0
        j = 0
        for x in range(self.size):
            for y in range(self.size):
                j += 1
                print(f"\rCleaning: {j}/{self.size ** 2}", end='')
                for i in range(3):
                    if i ==  0:
                        if self.top.isPresent(x,y):
                            self.top.remove(x,y)
                            if self.numConnected() < n:
                                self.top.add(x,y)
                            else:
                                rms += 1
                    if i ==  1:
                        if self.vias.isPresent(x,y):
                            self.vias.remove(x,y)
                            if self.numConnected() < n:
                                self.vias.add(x,y)
                            else:
                                rms += 1
                    if i ==  2:
                        if self.bottom.isPresent(x,y):
                            self.bottom.remove(x,y)
                            if self.numConnected() < n:
                                self.bottom.add(x,y)
                            else:
                                rms += 1
        print(f" - Removals {rms}")

    def print(self):
        for y in range(self.size):
            for x in range(self.size):
                t = self.top.isPresent(x,y)
                v = self.vias.isPresent(x,y)
                b = self.bottom.isPresent(x,y)
                s = (t,v,b)
                if s == (False,False,False):
                    print(".",end='')
                elif s == (True,False,False):
                    print("-",end='')
                elif s == (False,True,False):
                    print("X",end='')
                elif s == (True,True,False):
                    print("X",end='')
                elif s == (False,False,True):
                    print("|",end='')
                elif s == (True,False,True):
                    print("+",end='')
                elif s == (False,True,True):
                    print("X",end='')
                else:
                    # True, True, True
                    print("X",end='')
            print("")

fanouts = {
    (1,1) : [(19,19),(17,17)],
    (2,2) : [(18,18)],
    (2,4) : [(3,10)],
    #(5,1) : [(1,10)],
    (10,0): [(10,1)],
    (19,1) : [(19,8)],
    (10,10) : [(5,5)],
    #(4,4): [(8,8)],
    (8,5): [(5,8)],
}


print("")
size = 20
pcb = Pcb(size, fanouts)
pcb.search()

cs = pcb.listConnected()
ns = pcb.listNets()
xs = pcb.numCrossConnected()

print(f"Routed: {len(cs)}/{len(ns)}")
print(f"Cross connected: {xs}")

pcb.cleanUp()
pcb.print()

cs = pcb.listConnected()
ns = pcb.listNets()
xs = pcb.numCrossConnected()

print(f"Routed: {len(cs)}/{len(ns)}")
print(f"Cross connected: {xs}")






