import pcbnew

# RUN: exec(open("/Users/ashleyr/RTL-to-PCB/tools/python/loadPCB.py").read())

def addVia(x, y):
    b = pcbnew.GetBoard()
    v = pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.wxPointMM(x, y))
    v.SetDrill(int(0.4 * 1e6))
    v.SetWidth(int(0.8 * 1e6))
    b.Add(v)

def addTrace(sx, sy, ex, ey, top_n_bot=True, width=0.3):
    b = pcbnew.GetBoard()
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.wxPointMM(sx, sy))
    t.SetEnd(pcbnew.wxPointMM(ex, ey))
    t.SetWidth(int(width * 1e6))
    if top_n_bot:
        t.SetLayer(pcbnew.F_Cu)
    else:
        t.SetLayer(pcbnew.B_Cu)
    b.Add(t)

with open('/Users/ashleyr/RTL-to-PCB/counter_8_bit.pcb', 'r+') as f:
    pcb = f.read()

lines = pcb.split('\n')
size = len(lines)

top = []
via = []
bot = []
places = []
for y,line in enumerate(pcb.split('\n')):
    top.append([])
    via.append([])
    bot.append([])
    for x,pos in enumerate(line.split(",")):
        l = pos.split(":")
        top[y].append(int(l[0]))
        via[y].append(int(l[1]))
        bot[y].append(int(l[2]))

for y in range(size):
    for x in range(size-1):
        if (top[y][x] == top[y][x+1]) and (top[y][x] != -1):
            addTrace(x,y,x+1,y,True)

for x in range(size):
    for y in range(size-1):
        if (bot[y][x] == bot[y+1][x]) and (bot[y][x] != -1):
            addTrace(x,y,x,y+1,False)

for x in range(size):
    for y in range(size):
        if (via[y][x] != -1):
            addVia(x,y)


with open('/Users/ashleyr/RTL-to-PCB/counter_8_bit.place', 'r+') as f:
    place = f.read()

b = pcbnew.GetBoard()
places = []
for y,line in enumerate(place.split('\n')):
    places.append([])
    for x,name in enumerate(line.split(",")):
        if name != "":
            # Place the cell
            m = b.FindFootprintByReference(name)
            xs = (x * 15) + 2
            ys = (y * 15) + 7
            m.SetPosition(pcbnew.wxPointMM(xs,ys))

            if name[0] in ["N","D"]:
                # Input A track
                addTrace(xs,ys,xs+1,ys,True)
                addTrace(xs+1,ys,xs+1,ys-0.6,True)
                addVia(xs+1,ys-0.6)
                addTrace(xs+1,ys-0.6,xs+1,ys-3,False)

                # Input B track
                addTrace(xs,ys+0.65,xs+3,ys+0.65,True)
                addTrace(xs+3,ys+0.65,xs+4,ys-0.6,True)
                addVia(xs+4,ys-0.6)
                addTrace(xs+4,ys-0.6,xs+4,ys-3,False)

                # Output B track
                addTrace(xs+2,ys+1.3,xs+4,ys+1.3,True)
                addVia(xs+4,ys+1.3)
                addTrace(xs+4,ys+1.3,xs+4,ys+3.9,False)

                # VCC
                addTrace(xs-1.5,ys-0.3,xs-1.5,ys-1.8,True)
                addTrace(xs+2.2,ys,xs+2.2,ys-1.8,True)

                # GND
                addTrace(xs-1.5,ys+1.3,xs-1.5,ys+2.5,True)
                addTrace(xs,ys+1.3,xs,ys+2.5,True)

            elif name[0] == "I":
                addTrace(xs,ys,xs+4,ys,True)
                addVia(xs+4,ys)
                addTrace(xs+4,ys,xs+4,ys+3.9,False)

            elif name[0] == "O":
                addTrace(xs,ys,xs+2,ys,True)
                addVia(xs+2,ys)
                addTrace(xs+2,ys,xs+1,ys,False)
                addTrace(xs+1,ys,xs+1,ys-3,False)




for y,line in enumerate(place.split('\n')):
    start = -1
    end = -1
    for x,name in enumerate(line.split(",")):
        if name != "":
            if name[0] in ["D","N"]:
                if start == -1:
                    start = x
                end = x
    if end != -1:
        # Horizontal
        addTrace((start * 15)+0.6,(y*15)+5.2,size+3,(y*15)+5.2,True,1);
        addTrace(-3,(y*15)+9.5,(end * 15)+2,(y*15)+9.5,True,1);
# Vertical
addTrace(-3,9.5,-3,(y*15)+9.5,True,1);
addTrace(size+3,5.2,size+3,(y*15)+5.2,True,1);


pcbnew.Refresh()

