import pcbnew

# Origin
ORIG_X = 20
ORIG_Y = 20

# Placement
GRID_X = 5
GRID_Y = 5
PITCH_X = 7
PITCH_Y = 8

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


b = pcbnew.GetBoard()

# Place all parts
for x in range(1,GRID_X+1):
    for y in range(1,GRID_Y+1):
        d = (GRID_X * (y-1)) + x
        m = b.FindFootprintByReference(f"U{d}")
        if m is not None:
            m.SetPosition(pcbnew.wxPointMM(ORIG_X+(x*PITCH_X),ORIG_Y+(y*PITCH_Y)))

# VCC Copper pours
for y in range(GRID_Y):
    points = [
        pcbnew.wxPointMM(FINGER_VCC_ORIG_X, FINGER_VCC_ORIG_Y + (y * FINGER_VCC_PITCH)),
        pcbnew.wxPointMM(FINGER_VCC_ORIG_X + FINGER_VCC_LENGTH, FINGER_VCC_ORIG_Y + (y * FINGER_VCC_PITCH)),
        pcbnew.wxPointMM(FINGER_VCC_ORIG_X + FINGER_VCC_LENGTH, FINGER_VCC_ORIG_Y + (y * FINGER_VCC_PITCH) + FINGER_VCC_WIDTH),
        pcbnew.wxPointMM(FINGER_VCC_ORIG_X, FINGER_VCC_ORIG_Y + (y * FINGER_VCC_PITCH) + FINGER_VCC_WIDTH)
    ]
    z = pcbnew.ZONE(b)
    z.SetLayer(pcbnew.F_Cu)
    z.SetNetCode(b.GetNetsByName()['VDC'].GetNetCode())
    z.AddPolygon( pcbnew.wxPoint_Vector(points) )
    z.SetIsFilled(True)
    b.Add(z)

# GND Copper pours
for y in range(GRID_Y):
    points = [
        pcbnew.wxPointMM(FINGER_GND_ORIG_X, FINGER_GND_ORIG_Y + (y * FINGER_GND_PITCH)),
        pcbnew.wxPointMM(FINGER_GND_ORIG_X + FINGER_GND_LENGTH, FINGER_GND_ORIG_Y + (y * FINGER_GND_PITCH)),
        pcbnew.wxPointMM(FINGER_GND_ORIG_X + FINGER_GND_LENGTH, FINGER_GND_ORIG_Y + (y * FINGER_GND_PITCH) + FINGER_GND_WIDTH),
        pcbnew.wxPointMM(FINGER_GND_ORIG_X, FINGER_GND_ORIG_Y + (y * FINGER_GND_PITCH) + FINGER_GND_WIDTH)
    ]
    z = pcbnew.ZONE(b)
    z.SetLayer(pcbnew.F_Cu)
    z.SetNetCode(b.GetNetsByName()['GNDREF'].GetNetCode())
    z.AddPolygon( pcbnew.wxPoint_Vector(points) )
    z.SetIsFilled(True)
    b.Add(z)



# Take all updates
pcbnew.Refresh()

