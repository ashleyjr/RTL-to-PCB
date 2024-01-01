import pickle
import math
import random


def distance(cells,pos):
    d = 0
    for cell_a in cells:
        for cell_b in cells:
            if (cell_a[0] == "N") and (cell_b[0] == "N"):
                if (cells[cell_a]['Y'] == cells[cell_b]['A']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))
                    break
                if (cells[cell_a]['Y'] == cells[cell_b]['B']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))

            if (cell_a[0] == "D") and (cell_b[0] == "N"):
                if (cells[cell_a]['Q'] == cells[cell_b]['A']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))
                    break
                if (cells[cell_a]['Q'] == cells[cell_b]['B']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))

            if (cell_a[0] == "N") and (cell_b[0] == "D"):
                if (cells[cell_a]['Y'] == cells[cell_b]['D']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))

            if (cell_a[0] == "D") and (cell_b[0] == "D"):
                if (cells[cell_a]['Q'] == cells[cell_b]['D']):
                    x = abs(pos[cell_a]['x'] - pos[cell_b]['x'])
                    y = abs(pos[cell_a]['y'] - pos[cell_b]['y'])
                    d += math.sqrt((x * x) + (y * y))

    return d

with open('test.pkl', 'rb') as f:
    cells = pickle.load(f)

# Square grid
s = math.ceil(math.sqrt(len(cells)))
print(s)


best_idx = 0
poss = []

for i in range(100):
    # Layout in order
    x = 0
    y = 0
    pos = {}
    for cell in cells:
        pos[cell] = {}
        pos[cell]['x'] = x
        pos[cell]['y'] = y
        x += 1
        if x > s:
            x = 0
            y += 1


    # Random swaps
    last = distance(cells, pos)
    #print(last)
    for j in range(3000):
        a = random.choice(list(pos))
        b = random.choice(list(pos))
        temp = pos[a]
        pos[a] = pos[b]
        pos[b] = temp
        test = distance(cells, pos)
        if (test < last):
            last = test
            #print(f"{i} {test}")
        else:
            temp = pos[a]
            pos[a] = pos[b]
            pos[b] = temp


    if i == 0:
        best_score = last
        best_idx = 0
    else:
        if last < best_score:
            best_score = last
            best_idx = i

    poss.append(pos)
    print(f"{i}: [{best_idx}] {best_score}")

with open('place.pkl', 'wb') as f:
    pickle.dump(poss[best_idx], f)


