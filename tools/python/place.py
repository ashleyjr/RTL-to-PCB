import pickle
import math
import random
import sys

def distance(ass,pos):
    d = 0
    for net in ass:
        for cell_a in ass[net]:
            for cell_b in ass[net]:
                if cell_a != cell_b:
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))
    return d

def crosses(pairs, pos):
    c = 0
    for pair in pairs:
        if intersect(pos[pair[0]],pos[pair[1]],pos[pair[2]],pos[pair[3]]):
            c += 1
    return c

def furthestA(a,b):
    d_a = math.sqrt((a['x'] ** 2) + (a['y'] ** 2))
    d_b = math.sqrt((b['x'] ** 2) + (b['y'] ** 2))
    return (d_a > d_b)

def intersect(t_a0,t_a1,t_b0,t_b1):

    a0 = t_a0
    a1 = t_a1
    b0 = t_b0
    b1 = t_b1

    # Vertical lines
    a_v = (a0['x'] == a1['x'])
    b_v = (b0['x'] == b1['x'])

    if a_v and b_v:
        return False

    # Swap so moving away from origin
    if furthestA(a0,a1):
        t = a0
        a0 = a1
        a1 = t
    if furthestA(b0,b1):
        t = b0
        b0 = b1
        b1 = t

    if not a_v:
        m0 = (a1['y'] - a0['y']) / (a1['x'] - a0['x'])
        c0 = a0['y'] - (m0 * a0['x'])
        #print(f"A: y = {m0}x + {c0}")
    #else:
        #print(f"A: x = {a0['x']}")


    if not b_v:
        m1 = (b1['y'] - b0['y']) / (b1['x'] - b0['x'])
        c1 = b0['y'] - (m1 * b0['x'])
        #print(f"B: y = {m1}x + {c1}")
    #else:
        #print(f"AB: x = {b0['x']}")

    # Lines are parallel
    if not a_v and not b_v:
        if m0 == m1:
            # On same crossing point
            return (c0 == c1)

    # Calculate intersect
    p = {}
    if not a_v and not b_v:
        p['x'] = (c1 - c0) / (m0 - m1)
        p['y'] = (m0 * p['x']) + c0

    if a_v:
        p['x'] = a0['x']
        p['y'] = (m1 * p['x']) + c1

    if b_v:
        p['x'] = b0['x']
        p['y'] = (m0 * p['x']) + c0

    #print(f"Intersect: ({p['x']},{p['y']})")

    if (a1['x'] <= a0['x']):
        ax = (a0['x'] <= p['x']) and (p['x'] <= a1['x'])
    else:
        ax = (a1['x'] <= p['x']) and (p['x'] <= a0['x'])

    if (b1['x'] <= b0['x']):
        bx = (b0['x'] <= p['x']) and (p['x'] <= b1['x'])
    else:
        bx = (b1['x'] <= p['x']) and (p['x'] <= b0['x'])

    if (a1['y'] <= a0['y']):
        ay = (a0['y'] <= p['y']) and (p['y'] <= a1['y'])
    else:
        ay = (a1['y'] <= p['y']) and (p['y'] <= a0['y'])

    if (b1['y'] <= b0['y']):
        by = (b0['y'] <= p['y']) and (p['y'] <= b1['y'])
    else:
        by = (b1['y'] <= p['y']) and (p['y'] <= b0['y'])


    ##print(f"Check range: ax={ax}, bx={ax}, ay={ay}, by={by}")

    ## Check X axis range within intersect
    return (ax and bx and ay and by)


with open('test.pkl', 'rb') as f:
    cells = pickle.load(f)

# Square grid
sqr = math.ceil(math.sqrt(len(cells)))
print(sqr)

# Find all nets
all_nets = []
for n in cells:
    for s in cells[n]:
        net = cells[n][s]
        if net not in all_nets:
            all_nets.append(net)

# Association for each net
ass = {}
for n in all_nets:
    ass[n] = []
    for cell in cells:
        for pin in cells[cell]:
            if cells[cell][pin] == n:
                if cell not in ass[n]:
                    ass[n].append(cell)
for a in ass:
    print(ass[a])

# Collect all wire pairs
pairs = []
for net_a in ass:
    for net_b in ass:
        if net_a != net_b:
            p = []
            p.append(ass[net_a][0])
            p.append(ass[net_a][1])
            p.append(ass[net_b][0])
            p.append(ass[net_b][1])
            pairs.append(p)

# Layout in order
x = 0
y = 0
pos = {}
for cell in cells:
    pos[cell] = {}
    pos[cell]['x'] = x
    pos[cell]['y'] = y
    x += 1
    if x >= sqr:
        x = 0
        y += 1

start = len(cells)
for e in range(start, (sqr * sqr)):
    pos[f"empty_{e}"] = {}
    pos[f"empty_{e}"]['x'] = x
    pos[f"empty_{e}"]['y'] = y
    x += 1
    if x >= sqr:
        x = 0
        y += 1



# Random swaps
last_d = distance(ass, pos)
last_c = crosses(pairs, pos)
print(f"D={last_d:.2f} C={last_c}")
LIMIT=1000
for t in range(LIMIT):

    ps = list(pos)
    a = random.choice(ps)
    ps.remove(a)
    b = random.choice(ps)

    temp = pos[a]
    pos[a] = pos[b]
    pos[b] = temp

    test_d = distance(ass, pos)
    test_c = crosses(pairs, pos)

    if (test_c < last_c) or ((test_c == 0) and (test_d <= last_d)):
        last_c = test_c
        last_d = test_d
        print(f"{t} D={test_d:.2f} C={test_c}")
    else:
        # Swap back
        temp = pos[a]
        pos[a] = pos[b]
        pos[b] = temp

# Remove empty slots
final = {}
for p in pos:
    if "empty" not in p:
        final[p] = pos[p]
        print(f"{p}:{final[p]}")


for p0 in pos:
    for p1 in pos:
        if p0 != p1:
            assert pos[p0] != pos[p1]

with open('place.pkl', 'wb') as f:
    pickle.dump(final, f)



## Net routing
#vias = []
#for i in range(sqr * 3):
#    c = []
#    for j in range (sqr):
#        c.append(random.choice(list(ass)))
#    vias.append(c)
#    print(c)

# Create fanout dict for each net
fanouts = {}
for n in all_nets:
    sinks = {}
    src = None
    for cell in cells:
        for pin in cells[cell]:
            if cells[cell][pin] == n:
                if pin in ["Q","Y"]:
                    src = cell
                else:
                    sinks[cell] = pin
    if src == None:
        for s in sinks:
            if s[0] == "P":
                src = s
        sinks.pop(src, None)
    fanouts[src] = sinks

for f in fanouts:
    print(f"{f}:{fanouts[f]}")

with open('vias.pkl', 'wb') as f:
    pickle.dump(fanouts, f)






G = 10
front = [[False for x in range(sqr*G)] for y in range(sqr*G)]
front_keepout = [[False for x in range(sqr*G)] for y in range(sqr*G)]
bottom = [[False for x in range(sqr*G)] for y in range(sqr*G)]
bottom_keepout = [[False for x in range(sqr*G)] for y in range(sqr*G)]
vias = [[False for x in range(sqr*G)] for y in range(sqr*G)]
starts = [[None for x in range(sqr*G)] for y in range(sqr*G)]
ends = [[False for x in range(sqr*G)] for y in range(sqr*G)]

for f in fanouts:
    if f[0] == "P":
        net = cells[f]['A']
    if f[0] == "N":
        net = cells[f]['Y']
    starts[pos[f]['x']*G][pos[f]['y']*G] = net

for ff in fanouts:
    for f in ff:
        ends[pos[f]['x']*G][pos[f]['y']*G] = cells[f][ff[f]]




for ss in starts:
    for s in ss:
        if s != None:
            print(f"{s}",end='')
        else:
            print(' ',end='')
    print()





