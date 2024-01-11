import numpy as np
import random
import os
import math

class Grid:

    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
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
        s = []
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 0:
                    s.append((x,y))
        for _ in range(n):
            x,y = random.choice(s)
            self.grid[x][y] = 1#random.choice([0,1])
            s.remove((x,y))

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

    def __update(self, x, y, v):
        #if self.vert_n_horz:
        if self.grid[x][y] !=2:
            self.grid[x][y] = v
        #else:
        #    if self.grid[y][x] != 2:
        #        self.grid[y][x] = v

    def remove(self, x, y):
        self.__update(x ,y, 0)

    def add(self, x, y):
        self.__update(x, y, 1)

    def isPresent(self, x, y):
        #if self.vert_n_horz:
        return self.grid[x][y] == 1
        #else:
        #    return self.grid[y][x] == 1



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
        print(self.nets)

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
            while ((x,y) != (ex,ey)) or not top_n_bottom:
                #pcb.print()
                print(f"{x},{y},{ex},{ey}{top_n_bottom},{avoids}")
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
                        self.top.add(x,y)
                        if not top_n_bottom:
                            self.vias.add(x,y)
                        if self.numCrossConnected() == 0:
                            top_n_bottom = True
                            break
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
                        self.bottom.add(x,y)
                        if top_n_bottom:
                            self.vias.add(x,y)
                        if self.numCrossConnected() == 0:
                            top_n_bottom = False
                            break
                        self.bottom.remove(x,y)
                        if top_n_bottom:
                            self.vias.remove(x,y)
                        del bpos[i]
                        del bdis[i]
                        # Avoids this in the future
                        avoids.append((x,y))

            pcb.print()
            print(f"\r{n_i+1}/{len(self.nets)}")

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

    def growTop(self):
        self.grew_top = False
        grow = []
        for x in range(self.size):
            for y in range(self.size):
                # Grow top horizontal
                if self.top.isPresent(x,y):
                    if x != 0:
                        if not self.top.isPresent(x-1,y) and \
                            (x-1,y) not in grow:
                            grow.append((x-1,y))
                    if x != self.size-1:
                        if not self.top.isPresent(x+1,y) and \
                            (x+1,y) not in grow:
                            grow.append((x+1,y))
                # Add where vias appear
                if self.vias.isPresent(x,y):
                    if not self.top.isPresent(x,y) and \
                        (x,y) not in grow:
                        grow.append((x,y))
        # Also add some randoms
        x = random.randrange(self.size)
        y = random.randrange(self.size)
        grow.append((x,y))
        if len(grow) != 0:
            self.grew_top = True
            self.grow_xt,self.grow_yt = random.choice(grow)
            self.top.add(self.grow_xt,self.grow_yt)

    def growVias(self):
        self.grew_vias = False
        grow = []
        for x in range(self.size):
            for y in range(self.size):
                if self.top.isPresent(x,y) or\
                   self.bottom.isPresent(x,y):
                    grow.append((x,y))
        # Also add some randoms
        x = random.randrange(self.size)
        y = random.randrange(self.size)
        grow.append((x,y))
        if len(grow) != 0:
            self.grew_vias = True
            self.grow_xv,self.grow_yv = random.choice(grow)
            self.vias.add(self.grow_xv,self.grow_yv)


    def growBottom(self):
        self.grew_bottom = False
        grow = []
        # Favour nearby
        for x in range(self.size):
            for y in range(self.size):
                # Grow top horizontal
                if self.bottom.isPresent(x,y):
                    if y != 0:
                        if not self.bottom.isPresent(x,y-1) and \
                            (x,y-1) not in grow:
                            grow.append((x,y-1))
                    if y != self.size-1:
                        if not self.bottom.isPresent(x,y+1) and \
                            (x,y+1) not in grow:
                            grow.append((x,y+1))
                # Add where vias appear
                if self.vias.isPresent(x,y):
                    if not self.bottom.isPresent(x,y) and \
                        (x,y) not in grow:
                        grow.append((x,y))
        # Also add some randoms
        x = random.randrange(self.size)
        y = random.randrange(self.size)
        grow.append((x,y))
        # Select
        if len(grow) != 0:
            self.grew_bottom = True
            self.grow_xb,self.grow_yb = random.choice(grow)
            self.bottom.add(self.grow_xb,self.grow_yb)

    def grow(self):
        self.growTop()
        self.growVias()
        self.growBottom()

    def undoGrow(self):
        if self.grew_top:
            self.top.remove(self.grow_xt, self.grow_yt)
        if self.grew_vias:
            self.vias.remove(self.grow_xv, self.grow_yv)
        if self.grew_bottom:
            self.bottom.remove(self.grow_xb, self.grow_yb)

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

    def lenConnected(self, x0, y0, x1, y1):
        t,_,b = self.path(x0,y0,x1,y1)
        l = len(t)
        l += len(b)
        return l

    def numNets(self):
        return len(self.nets)

    def numConnected(self):
        num = 0
        print(self.nets)
        for sx,sy,ex,ey in self.nets:
            if self.isConnected(sx,sy,ex,ey):
                num += 1
        return num

    def totalLenConnected(self):
        l = 0
        for sx,sy,ex,ey in self.nets:
            if self.isConnected(sx,sy,ex,ey):
                l += self.lenConnected(sx,sy,ex,ey)
        return l

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
        for x in range(self.size):
            print(x)
            for y in range(self.size):
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

    def ripUpCrossConnected(self):
        # All the bad connections
        bads = self.listCrossConnected()
        print(bads)
        tbads = []
        vbads = []
        bbads = []
        for sx,sy,ex,ey in bads:
            self.printPath(sx,sy,ex,ey)
            ts,vs,bs = self.path(sx, sy, ex, ey)
            tbads += ts
            vbads += vs
            bbads += bs
        # All the good connections
        goods = self.listConnected()
        print(goods)
        tgoods = []
        vgoods = []
        bgoods = []
        for sx,sy,ex,ey in goods:
            self.printPath(sx,sy,ex,ey)
            ts,vs,bs = self.path(sx, sy, ex, ey)
            tgoods += ts
            vgoods += vs
            bgoods += bs
        # Add the good ones back
        for t in tgoods:
            if t in tbads:
                tbads.remove(t)
        for v in bgoods:
            if v in vbads:
                vbads.remove(v)
        for b in bgoods:
            if b in bbads:
                bbads.remove(b)
        print(tbads)
        print(vbads)
        print(bbads)
        # Make the removes
        for x,y in tbads:
            self.top.remove(x,y)
        for x,y in vbads:
            self.vias.remove(x,y)
        for x,y in bbads:
            self.bottom.remove(x,y)
        breakpoint()



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

    def printPaths(self):
        for sx,sy,ex,ey in self.nets:
            if self.isConnected(sx,sy,ex,ey):
                print("")
                t,v,b = self.path(sx,sy,ex,ey)
                print(f"T:{t}")
                print(f"V:{v}")
                print(f"B:{b}")

    def printPath(self,sx,sy,ex,ey):
        print("")
        t,v,b = self.path(sx,sy,ex,ey)
        print(f"T:{t}")
        print(f"V:{v}")
        print(f"B:{b}")

    def path(self, x0, y0, x1, y1):
        '''
        Check if two points are connected.
        Start and ends on the top layer,
        Even hopcounts == top
        Odd hopcount == bottom
        '''
        assert self.isConnected(x0,y0,x1,y1)
        to_pop = 1
        stack = [(x0,y0)]
        found = False
        nest = []
        for hopcount in range(self.size * self.size):
            end = len(stack)
            start = end - to_pop
            to_pop = 0
            nest.append({})
            for s in range(start,end):
                x,y = stack[s]
                nest[hopcount][(x,y)] = []
                for i in range(self.size):
                    for j in range(self.size):
                        c = (i,j)
                        if (x,y) != c:
                            # TODO: Vias indexing appears the wrong way round
                            if (hopcount % 2) == 0:
                                if self.top.isConnected(x,y,i,j):
                                    if c == (x1,y1):
                                        print("c")
                                        nest[hopcount][(x,y)].append(c)
                                        found = True
                                    if self.vias.isPresent(i,j) and (c not in stack):
                                        stack.append(c)
                                        nest[hopcount][(x,y)].append(c)
                                        to_pop += 1
                            else:
                                con = self.bottom.isConnected(x,y,i,j)
                                via = self.vias.isPresent(i,j)
                                if con and via and (c not in stack):
                                    stack.append(c)
                                    nest[hopcount][(x,y)].append((i,j))
                                    to_pop += 1
            if found:
                break

        t = [(x1,y1)]
        b = []
        v = []
        xf = x1
        yf = y1

        for hopcount in range(len(nest)-1,-1,-1):
            for start in nest[hopcount]:
                for end in nest[hopcount][start]:
                    if end == (xf,yf):
                        (xf,yf) = start
                        if (hopcount % 2) == 0:
                            t += self.top.path(start[0],start[1],end[0],end[1])
                        else:
                            b += self.bottom.path(start[0],start[1],end[0],end[1])
                        v.append(end)

        return (t,v,b)

    def permutateTop(self, n):
        self.top.permutate(n)

    def undoPermutateTop(self):
        self.top.undoPermutate()

    def permutateVias(self, n):
        self.vias.permutate(n)

    def undoPermutateVias(self):
        self.vias.undoPermutate()

    def permutateBottom(self, n):
        self.bottom.permutate(n)

    def undoPermutateBottom(self):
        self.bottom.undoPermutate()





fanouts = {
    (1,1) : [(19,19),(17,17)],
    (2,2) : [(18,18)],
    (2,4) : [(3,10)],
    (5,1) : [(1,10)],
    #(10,0): [(10,1)],
    #(19,1) : [(19,8)],
    #(10,10) : [(5,5)],
    (4,4): [(8,8)],
    #(8,5): [(5,8)],
}





print("")
size = 20
pcb = Pcb(size, fanouts)
pcb.print()
pcb.search()
pcb.print()
#print(pcb.isConnected(1,1,2,1))

c = pcb.numConnected()
#l = pcb.totalLenConnected()
n = pcb.numCrossConnected()
print(f"\r{c},{n}")



#i=0
#r=0
#while((n_last != 0) or (c_last != pcb.numNets())):
#
#
#    pcb.grow()
#    #pcb.permutateTop(1)
#    #pcb.permutateVias(1)
#    #pcb.permutateBottom(1)
#    c = pcb.numConnected()
#    l = pcb.totalLenConnected()
#    n = pcb.numCrossConnected()
#    keep = True
#
#    if (c < c_last):
#        pcb.undoGrow()
#    else:
#        if(n > 0):
#            pcb.ripUpCrossConnected()
#            pcb.addStartEnds()
#        else:
#            c_last = c
#            n_last = n
#            l_last = l
#
#    os.system('clear')
#    pcb.print()
#    print(f"\r{i},{r},{l},{c},{n}",end='')
#    #pcb.printPaths()
#    i+=1
#pcb.cleanUp()
#pcb.print()
