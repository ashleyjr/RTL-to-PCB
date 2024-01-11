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
        return (self.lenConnected(x0,y0,x1,y1) > 0)

    def path(self, x0, y0, x1, y1):
        assert self.isConnected(x0, y0, x1, y1)
        p = []
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
        for i in range(s,e+1):
            if self.vert_n_horz:
                if self.grid[a0][i] == 1:
                    p.append((a0,i))
            else:
                if self.grid[i][a0] == 1:
                    p.append((i,a0))
        print(p)
        return p

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
        self.addStartEnds()
        for sx,sy in fanouts:
            for ex,ey in fanouts[(sx,sy)]:
                self.nets.append((sx,sy,ex,ey))
        self.addStartEnds()

    def listNets(self):
        return self.nets

    def distance(self,x0,y0,x1,y1):
        x = abs(x0 - x1)
        y = abs(y0 - y1)
        d = (x ** 2) + (y ** 2)
        return math.sqrt(d)

    def search(self):
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
                print(f"\rNet: {sx},{ey},{ex},{ey},{x},{y},{top_n_bottom},{n_i},{move},{avoids}",end='')

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

                        if self.numCrossConnected() == 0:
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

                        if self.numCrossConnected() == 0:
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
        to_pop = 1
        stack = [(x0,y0)]
        #print(f"{x1},{y1}")
        for hopcount in range(self.size * self.size):
            end = len(stack)
            start = end - to_pop
            to_pop = 0
            for s in range(start,end):
                x,y = stack[s]
                for i in range(self.size):
                    for j in range(self.size):
                        c = (i,j)
                        #if (x,y) != c:
                        if (hopcount % 2) == 0:
                            #print(f"{x},{y},{i},{j}")
                            #print(c)
                            if self.top.isConnected(x,y,i,j):
                                #print("d")
                                if c == (x1,y1):
                                    #print("c")
                                    return True
                                if self.vias.isPresent(i,j):
                                    #print("v")
                                    if (c not in stack) or (x,y == c):
                                        stack.append(c)
                                        to_pop += 1
                        else:
                            con = self.bottom.isConnected(x,y,i,j)
                            via = self.vias.isPresent(i,j)
                            if con and via and (c not in stack):
                                #print("b")
                                stack.append(c)
                                to_pop += 1
            #print(stack)
            #print(to_pop)
            if to_pop == 0:
                return False
        # hopcoount
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

    def numCrossConnected(self):
        return len(self.listCrossConnected())

    def listCrossConnected(self):
        checks = []
        l = []
        for sx,sy in self.fanouts:
            for ex,ey in self.fanouts:
                if (sx,sy) != (ex,ey):
                    if (ex,ey,sx,sy) not in checks:
                        checks.append((sx,sy,ex,ey))
                    for x,y in self.fanouts[(ex,ey)]:
                        if (ex,ey,sx,sy) not in checks:
                            checks.append((sx,sy,x,y))

        for sx,sy,ex,ey in checks:
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
        j = 0
        for x in range(self.size):
            for y in range(self.size):
                print(f"\rCleaning: {j}/{self.size ** 2}", end='')
                j += 1
                for i in range(3):
                    if i ==  0:
                        self.top.remove(x,y)
                        if self.numConnected() < n:
                            self.top.add(x,y)
                    if i ==  1:
                        self.vias.remove(x,y)
                        if self.numConnected() < n:
                            self.vias.add(x,y)
                    if i ==  2:
                        self.bottom.remove(x,y)
                        if self.numConnected() < n:
                            self.bottom.add(x,y)

    def print(self):
        print("\nTOP                  VIAS                  BOTTOM")
        for y in range(self.size):
            for i in range(3):
                for x in range(self.size):
                    if i == 0:
                        if self.top.isPresent(x,y):
                            print("-",end='')
                        else:
                            print("O",end='')
                    if i == 1:
                        if self.vias.isPresent(x,y):
                            print("X",end='')
                        else:
                            print(",",end='')
                    if i == 2:
                        if self.bottom.isPresent(x,y):
                            print("|",end='')
                        else:
                            print("O",end='')
                print(" ",end='')
            print("")

#fanouts = {
#    (1,1) : [(19,19),(17,17)],
#    (2,2) : [(18,18)],
#    (2,4) : [(3,10)],
#    (5,1) : [(1,10)],
#    (10,0): [(10,1)],
#    (19,1) : [(19,8)],
#    (10,10) : [(5,5)],
#    (4,4): [(8,8)],
#    (8,5): [(5,8)],
#}
#
#
#print("")
#size = 20
#pcb = Pcb(size, fanouts)
#pcb.search()
#
#cs = pcb.listConnected()
#ns = pcb.listNets()
#xs = pcb.numCrossConnected()
#
#print(f"Routed: {len(cs)}/{len(ns)}")
#print(f"Cross connected: {xs}")
#
#pcb.cleanUp()
#pcb.print()
#
#cs = pcb.listConnected()
#ns = pcb.listNets()
#xs = pcb.numCrossConnected()
#
#print(f"Routed: {len(cs)}/{len(ns)}")
#print(f"Cross connected: {xs}")






