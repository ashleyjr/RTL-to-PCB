import pcbnew

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

with open('/Users/ashleyr/RTL-to-PCB/counter_4_bit.pcb', 'r+') as f:
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
        print(l)
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


with open('/Users/ashleyr/RTL-to-PCB/counter_4_bit.place', 'r+') as f:
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
                addTrace(xs+2.2,ys,xs+2.2,ys-1.8,True)

                # GND
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




for y in range(0,size,15):
    # Horizontal
    addTrace(0,y+5.2,size+3,y+5.2,True,1);
    addTrace(-3,y+9.5,size,y+9.5,True,1);
# Vertical
addTrace(-3,9.5,-3,y+9.5,True,1);
addTrace(size+3,5.2,size+3,y+5.2,True,1);


pcbnew.Refresh()

#import pickle
#
## Origin
#ORIG_X = 40
#ORIG_Y = 40
#
## Placement
#GRID_X = 6
#GRID_Y = 5
#PITCH_X = 6
#PITCH_Y = 11
#
## Power fingers
#FINGER_VCC_ORIG_X = 20
#FINGER_VCC_ORIG_Y = 25
#FINGER_VCC_WIDTH = 2
#FINGER_VCC_LENGTH = 38
#FINGER_VCC_PITCH = 8
#
#FINGER_GND_ORIG_X = 25
#FINGER_GND_ORIG_Y = 30.2
#FINGER_GND_WIDTH = 2
#FINGER_GND_LENGTH = 38
#FINGER_GND_PITCH = 8
#
#VERT_PER_CELL = 4
#VERT_PITCH = 1.1
#HORZ_PER_ROW = 4
#HORZ_PITCH = 1.1
#
#b = pcbnew.GetBoard()
#
#
#with open('/Users/ashleyr/RTL-to-PCB/place.pkl', 'rb') as f:
#    pos = pickle.load(f)
#
#with open('/Users/ashleyr/RTL-to-PCB/test.pkl', 'rb') as f:
#    cells = pickle.load(f)
#
#with open('/Users/ashleyr/RTL-to-PCB/vias.pkl', 'rb') as f:
#    vias = pickle.load(f)
#
#size_x = 0
#size_y = 0
#gnd_left_stops = {}
#vcc_right_stops = {}
#for p in pos:
#    size_x = max([pos[p]['x'], size_x])
#    size_y = max([pos[p]['y'], size_y])
#
#    x = ORIG_X + (pos[p]['x'] * PITCH_X)
#    y = ORIG_Y + (pos[p]['y'] * PITCH_Y)
#    if p[0] == "P":
#        x += 1.1
#        y += 0.75
#
#    m = b.FindFootprintByReference(p)
#    m.SetPosition(pcbnew.wxPointMM(x,y))
#
#    if p[0] in ["N", "D"]:
#
#        if (pos[p]['y'] not in gnd_left_stops) or\
#           (pos[p]['x'] < gnd_left_stops[pos[p]['y']]):
#            gnd_left_stops[pos[p]['y']] = pos[p]['x']
#
#        if (pos[p]['y'] not in vcc_right_stops) or\
#           (pos[p]['x'] > vcc_right_stops[pos[p]['y']]):
#            vcc_right_stops[pos[p]['y']] = pos[p]['x']
#
#        # GND taps
#        t = pcbnew.PCB_TRACK(b)
#        y += 1.336
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y += 1
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)
#
#        # VCC taps
#        t = pcbnew.PCB_TRACK(b)
#        y -= 2.336
#        x += 2.21
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y -= 1
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)
#
# GND rails
#for g in gnd_left_stops:
#    t = pcbnew.PCB_TRACK(b)
#    y = ORIG_Y + (g * PITCH_Y) + 2.336
#    x = ORIG_X + (gnd_left_stops[g] * PITCH_X)
#    t.SetStart(pcbnew.wxPointMM(x, y))
#    x = ORIG_X + ((size_x + 1) * PITCH_X)
#    t.SetEnd(pcbnew.wxPointMM(x, y))
#    t.SetWidth(int(0.7 * 1e6))
#    t.SetLayer(pcbnew.F_Cu)
#    b.Add(t)

## VCC rails
#for v in vcc_right_stops:
#    t = pcbnew.PCB_TRACK(b)
#    x = ORIG_X - PITCH_X
#    y = ORIG_Y + (v * PITCH_Y) - 1
#    t.SetStart(pcbnew.wxPointMM(x, y))
#    x = ORIG_X + (vcc_right_stops[v] * PITCH_X) + 2.21
#    t.SetEnd(pcbnew.wxPointMM(x, y))
#    t.SetWidth(int(0.7 * 1e6))
#    t.SetLayer(pcbnew.F_Cu)
#    b.Add(t)
#
## GND stantion
#t = pcbnew.PCB_TRACK(b)
#x = ORIG_X + ((size_x + 1) * PITCH_X)
#y = ORIG_Y +  2.336
#t.SetStart(pcbnew.wxPointMM(x, y))
#y = ORIG_Y + (size_y * PITCH_Y) + 2.336
#t.SetEnd(pcbnew.wxPointMM(x, y))
#t.SetWidth(int(1.4 * 1e6))
#t.SetLayer(pcbnew.F_Cu)
#b.Add(t)
#
## VCC stantion
#t = pcbnew.PCB_TRACK(b)
#x = ORIG_X - PITCH_X
#y = ORIG_Y - 1
#t.SetStart(pcbnew.wxPointMM(x, y))
#y = ORIG_Y + (size_y * PITCH_Y) - 1
#t.SetEnd(pcbnew.wxPointMM(x, y))
#t.SetWidth(int(1.4 * 1e6))
#t.SetLayer(pcbnew.F_Cu)
#b.Add(t)
#
## Cell vias
#for cell in cells:
#    if cell[0] == "P":
#        # Tap track
#        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
#        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
#        x += 1.1
#        y += 0.75
#        t = pcbnew.PCB_TRACK(b)
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        x -= 2.6
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#        # Row breakout track
#        t = pcbnew.PCB_TRACK(b)
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y += 2.55
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.B_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#
#    if cell[0] == "N":
#
#        ## Turn all NORs in to NOTs where possible by bridging two inputs
#        if cells[cell]["A"] == cells[cell]["B"]:
#            # Bridge track
#            x = ORIG_X + (pos[cell]['x'] * PITCH_X)
#            y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
#            t = pcbnew.PCB_TRACK(b)
#            t.SetStart(pcbnew.wxPointMM(x, y))
#            y += 0.65
#            t.SetEnd(pcbnew.wxPointMM(x, y))
#            t.SetWidth(int(0.3 * 1e6))
#            t.SetLayer(pcbnew.F_Cu)
#            b.Add(t)
#
#        # Input A track
#        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
#        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
#        t = pcbnew.PCB_TRACK(b)
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        x -= 1.5
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#        # Row breakout track
#        t = pcbnew.PCB_TRACK(b)
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y -= 2
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.B_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#
#        ## Bring out vias for all other gates
#        if cells[cell]["A"] != cells[cell]["B"]:
#
#            # Input B track
#            x = ORIG_X + (pos[cell]['x'] * PITCH_X)
#            y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
#            t = pcbnew.PCB_TRACK(b)
#            y += 0.65
#            t.SetStart(pcbnew.wxPointMM(x, y))
#            x += 2.85
#            t.SetEnd(pcbnew.wxPointMM(x, y))
#            t.SetWidth(int(0.3 * 1e6))
#            t.SetLayer(pcbnew.F_Cu)
#            b.Add(t)
#            t = pcbnew.PCB_TRACK(b)
#            t.SetStart(pcbnew.wxPointMM(x, y))
#            x += 0.65
#            y -= 0.65
#            t.SetEnd(pcbnew.wxPointMM(x, y))
#            t.SetWidth(int(0.3 * 1e6))
#            t.SetLayer(pcbnew.F_Cu)
#            b.Add(t)
#            # Add via
#            via = pcbnew.PCB_VIA(b)
#            via.SetPosition(pcbnew.wxPointMM(x, y))
#            via.SetDrill(int(0.4 * 1e6))
#            via.SetWidth(int(0.8 * 1e6))
#            b.Add(via)
#            # Row breakout track
#            t = pcbnew.PCB_TRACK(b)
#            t.SetStart(pcbnew.wxPointMM(x, y))
#            y -= 2
#            t.SetEnd(pcbnew.wxPointMM(x, y))
#            t.SetWidth(int(0.3 * 1e6))
#            t.SetLayer(pcbnew.B_Cu)
#            b.Add(t)
#            # Add via
#            via = pcbnew.PCB_VIA(b)
#            via.SetPosition(pcbnew.wxPointMM(x, y))
#            via.SetDrill(int(0.4 * 1e6))
#            via.SetWidth(int(0.8 * 1e6))
#            b.Add(via)
#
#        ## Bring VIAs out of all gate outputs
#        # Bridge track
#        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
#        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
#        t = pcbnew.PCB_TRACK(b)
#        x += 2.21
#        y += 1.3
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        x += 1.29
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#        # Row breakout track
#        t = pcbnew.PCB_TRACK(b)
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y += 2
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.B_Cu)
#        b.Add(t)
#        # Add via
#        via = pcbnew.PCB_VIA(b)
#        via.SetPosition(pcbnew.wxPointMM(x, y))
#        via.SetDrill(int(0.4 * 1e6))
#        via.SetWidth(int(0.8 * 1e6))
#        b.Add(via)
#
### Vertical routing grid
##for v in range(size_x + 1):
##    for o in range(VERT_PER_CELL):
##        t = pcbnew.PCB_TRACK(b)
##        x = ORIG_X + (v * PITCH_X) + (o * VERT_PITCH) - 0.6
##        y = ORIG_Y - 4
##        t.SetStart(pcbnew.wxPointMM(x, y))
##        y = ORIG_Y + (size_y * PITCH_Y) + 5.1
##        t.SetEnd(pcbnew.wxPointMM(x, y))
##        t.SetWidth(int(0.3 * 1e6))
##        t.SetLayer(pcbnew.B_Cu)
##        b.Add(t)
##
##
### Horizontal routing grid
##for v in range(size_y + 2):
##    for o in range(HORZ_PER_ROW):
##        t = pcbnew.PCB_TRACK(b)
##        x = ORIG_X - 0.6
##        y = ORIG_Y + ((v - 1) * PITCH_Y) + (o * HORZ_PITCH) + 4.05
##        t.SetStart(pcbnew.wxPointMM(x, y))
##        x = ORIG_X + (size_x * PITCH_X) + (HORZ_PITCH * (VERT_PER_CELL-1))
##        t.SetEnd(pcbnew.wxPointMM(x, y))
##        t.SetWidth(int(0.3 * 1e6))
##        t.SetLayer(pcbnew.F_Cu)
##        b.Add(t)
#
#
#
#
## Take all updates
#pcbnew.Refresh()

