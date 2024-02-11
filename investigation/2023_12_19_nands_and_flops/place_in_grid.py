import pcbnew
import pickle

# Origin
ORIG_X = 40
ORIG_Y = 40

# Placement
GRID_X = 6
GRID_Y = 5
PITCH_X = 6
PITCH_Y = 11

# Power fingers
FINGER_VCC_ORIG_X = 20
FINGER_VCC_ORIG_Y = 25
FINGER_VCC_WIDTH = 2
FINGER_VCC_LENGTH = 38
FINGER_VCC_PITCH = 8

FINGER_GND_ORIG_X = 25
FINGER_GND_ORIG_Y = 30.2
FINGER_GND_WIDTH = 2
FINGER_GND_LENGTH = 38
FINGER_GND_PITCH = 8

VERT_PER_CELL = 4
VERT_PITCH = 1.1
HORZ_PER_ROW = 4
HORZ_PITCH = 1.1

b = pcbnew.GetBoard()


with open('/Users/ashleyr/RTL-to-PCB/place.pkl', 'rb') as f:
    pos = pickle.load(f)

with open('/Users/ashleyr/RTL-to-PCB/test.pkl', 'rb') as f:
    cells = pickle.load(f)

with open('/Users/ashleyr/RTL-to-PCB/vias.pkl', 'rb') as f:
    vias = pickle.load(f)

size_x = 0
size_y = 0
gnd_left_stops = {}
vcc_right_stops = {}
for p in pos:
    size_x = max([pos[p]['x'], size_x])
    size_y = max([pos[p]['y'], size_y])

    x = ORIG_X + (pos[p]['x'] * PITCH_X)
    y = ORIG_Y + (pos[p]['y'] * PITCH_Y)
    if p[0] == "P":
        x += 1.1
        y += 0.75

    m = b.FindFootprintByReference(p)
    m.SetPosition(pcbnew.wxPointMM(x,y))

    if p[0] in ["N", "D"]:

        if (pos[p]['y'] not in gnd_left_stops) or\
           (pos[p]['x'] < gnd_left_stops[pos[p]['y']]):
            gnd_left_stops[pos[p]['y']] = pos[p]['x']

        if (pos[p]['y'] not in vcc_right_stops) or\
           (pos[p]['x'] > vcc_right_stops[pos[p]['y']]):
            vcc_right_stops[pos[p]['y']] = pos[p]['x']

        # GND taps
        t = pcbnew.PCB_TRACK(b)
        y += 1.336
        t.SetStart(pcbnew.wxPointMM(x, y))
        y += 1
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        b.Add(t)

        # VCC taps
        t = pcbnew.PCB_TRACK(b)
        y -= 2.336
        x += 2.21
        t.SetStart(pcbnew.wxPointMM(x, y))
        y -= 1
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        b.Add(t)

# GND rails
for g in gnd_left_stops:
    t = pcbnew.PCB_TRACK(b)
    y = ORIG_Y + (g * PITCH_Y) + 2.336
    x = ORIG_X + (gnd_left_stops[g] * PITCH_X)
    t.SetStart(pcbnew.wxPointMM(x, y))
    x = ORIG_X + ((size_x + 1) * PITCH_X)
    t.SetEnd(pcbnew.wxPointMM(x, y))
    t.SetWidth(int(0.7 * 1e6))
    t.SetLayer(pcbnew.F_Cu)
    b.Add(t)

# VCC rails
for v in vcc_right_stops:
    t = pcbnew.PCB_TRACK(b)
    x = ORIG_X - PITCH_X
    y = ORIG_Y + (v * PITCH_Y) - 1
    t.SetStart(pcbnew.wxPointMM(x, y))
    x = ORIG_X + (vcc_right_stops[v] * PITCH_X) + 2.21
    t.SetEnd(pcbnew.wxPointMM(x, y))
    t.SetWidth(int(0.7 * 1e6))
    t.SetLayer(pcbnew.F_Cu)
    b.Add(t)

# GND stantion
t = pcbnew.PCB_TRACK(b)
x = ORIG_X + ((size_x + 1) * PITCH_X)
y = ORIG_Y +  2.336
t.SetStart(pcbnew.wxPointMM(x, y))
y = ORIG_Y + (size_y * PITCH_Y) + 2.336
t.SetEnd(pcbnew.wxPointMM(x, y))
t.SetWidth(int(1.4 * 1e6))
t.SetLayer(pcbnew.F_Cu)
b.Add(t)

# VCC stantion
t = pcbnew.PCB_TRACK(b)
x = ORIG_X - PITCH_X
y = ORIG_Y - 1
t.SetStart(pcbnew.wxPointMM(x, y))
y = ORIG_Y + (size_y * PITCH_Y) - 1
t.SetEnd(pcbnew.wxPointMM(x, y))
t.SetWidth(int(1.4 * 1e6))
t.SetLayer(pcbnew.F_Cu)
b.Add(t)

# Cell vias
for cell in cells:
    if cell[0] == "P":
        # Tap track
        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
        x += 1.1
        y += 0.75
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.wxPointMM(x, y))
        x -= 2.6
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)
        # Row breakout track
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.wxPointMM(x, y))
        y += 2.55
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.B_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)

    if cell[0] == "N":

        ## Turn all NORs in to NOTs where possible by bridging two inputs
        if cells[cell]["A"] == cells[cell]["B"]:
            # Bridge track
            x = ORIG_X + (pos[cell]['x'] * PITCH_X)
            y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.wxPointMM(x, y))
            y += 0.65
            t.SetEnd(pcbnew.wxPointMM(x, y))
            t.SetWidth(int(0.3 * 1e6))
            t.SetLayer(pcbnew.F_Cu)
            b.Add(t)

        # Input A track
        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.wxPointMM(x, y))
        x -= 1.5
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)
        # Row breakout track
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.wxPointMM(x, y))
        y -= 2
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.B_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)

        ## Bring out vias for all other gates
        if cells[cell]["A"] != cells[cell]["B"]:

            # Input B track
            x = ORIG_X + (pos[cell]['x'] * PITCH_X)
            y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
            t = pcbnew.PCB_TRACK(b)
            y += 0.65
            t.SetStart(pcbnew.wxPointMM(x, y))
            x += 2.85
            t.SetEnd(pcbnew.wxPointMM(x, y))
            t.SetWidth(int(0.3 * 1e6))
            t.SetLayer(pcbnew.F_Cu)
            b.Add(t)
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.wxPointMM(x, y))
            x += 0.65
            y -= 0.65
            t.SetEnd(pcbnew.wxPointMM(x, y))
            t.SetWidth(int(0.3 * 1e6))
            t.SetLayer(pcbnew.F_Cu)
            b.Add(t)
            # Add via
            via = pcbnew.PCB_VIA(b)
            via.SetPosition(pcbnew.wxPointMM(x, y))
            via.SetDrill(int(0.4 * 1e6))
            via.SetWidth(int(0.8 * 1e6))
            b.Add(via)
            # Row breakout track
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.wxPointMM(x, y))
            y -= 2
            t.SetEnd(pcbnew.wxPointMM(x, y))
            t.SetWidth(int(0.3 * 1e6))
            t.SetLayer(pcbnew.B_Cu)
            b.Add(t)
            # Add via
            via = pcbnew.PCB_VIA(b)
            via.SetPosition(pcbnew.wxPointMM(x, y))
            via.SetDrill(int(0.4 * 1e6))
            via.SetWidth(int(0.8 * 1e6))
            b.Add(via)

        ## Bring VIAs out of all gate outputs
        # Bridge track
        x = ORIG_X + (pos[cell]['x'] * PITCH_X)
        y = ORIG_Y + (pos[cell]['y'] * PITCH_Y)
        t = pcbnew.PCB_TRACK(b)
        x += 2.21
        y += 1.3
        t.SetStart(pcbnew.wxPointMM(x, y))
        x += 1.29
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.F_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)
        # Row breakout track
        t = pcbnew.PCB_TRACK(b)
        t.SetStart(pcbnew.wxPointMM(x, y))
        y += 2
        t.SetEnd(pcbnew.wxPointMM(x, y))
        t.SetWidth(int(0.3 * 1e6))
        t.SetLayer(pcbnew.B_Cu)
        b.Add(t)
        # Add via
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.wxPointMM(x, y))
        via.SetDrill(int(0.4 * 1e6))
        via.SetWidth(int(0.8 * 1e6))
        b.Add(via)

## Vertical routing grid
#for v in range(size_x + 1):
#    for o in range(VERT_PER_CELL):
#        t = pcbnew.PCB_TRACK(b)
#        x = ORIG_X + (v * PITCH_X) + (o * VERT_PITCH) - 0.6
#        y = ORIG_Y - 4
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        y = ORIG_Y + (size_y * PITCH_Y) + 5.1
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.B_Cu)
#        b.Add(t)
#
#
## Horizontal routing grid
#for v in range(size_y + 2):
#    for o in range(HORZ_PER_ROW):
#        t = pcbnew.PCB_TRACK(b)
#        x = ORIG_X - 0.6
#        y = ORIG_Y + ((v - 1) * PITCH_Y) + (o * HORZ_PITCH) + 4.05
#        t.SetStart(pcbnew.wxPointMM(x, y))
#        x = ORIG_X + (size_x * PITCH_X) + (HORZ_PITCH * (VERT_PER_CELL-1))
#        t.SetEnd(pcbnew.wxPointMM(x, y))
#        t.SetWidth(int(0.3 * 1e6))
#        t.SetLayer(pcbnew.F_Cu)
#        b.Add(t)




# Take all updates
pcbnew.Refresh()

