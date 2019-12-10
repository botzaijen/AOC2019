import math
from itertools import cycle

def readMapToRowColList(filename):
    with open(filename, "r") as f:
        rowcolmap = [line.strip() for line in f]
    return rowcolmap

def rowColMapToAsteroidCoord(rowcolmap):
    coords = []
    for y, row in enumerate(rowcolmap):
        for x, c in enumerate(row):
            if c == '#':
                coords.append((x,y))
    return coords

def compute_hcf(x, y):
   while(y):
       x, y = y, x % y
   return x

def clockwiseOrd(coord):
    x,y = coord
    v = math.atan2(y,x) + math.pi/2
    if v < 0:
        v = 2*math.pi + v
    return v

def countVisible(coords, ori_idx):
    ox, oy = coords[ori_idx]
    hitlist = []
    for i, coord in enumerate(coords):
        if i == ori_idx:
            continue
        x,y = coord
        dx = x-ox
        dy = y-oy
        hcf = compute_hcf(dx,dy)
        if hcf < 0:
            hcf = -hcf
        hitlist.append((dx/hcf, dy/hcf)) 
    return len(set(hitlist))


def part1(filename):
    rcm = readMapToRowColList(filename)
    coords = rowColMapToAsteroidCoord(rcm)
    counts = []
    invc = {}
    for idx, ast in enumerate(coords):
        c = countVisible(coords, idx)
        counts.append((c, ast, idx))
        invc[ast] = c
    counts.sort(key=lambda tup: tup[0])
    print(counts[-1])
    return counts[-1]

def part2(filename, ori, ori_idx):
    #ori = (11,19) # answer part1
    #ori_idx = 270 # answer part1
    rcm = readMapToRowColList(filename)
    coords = rowColMapToAsteroidCoord(rcm)
    del coords[ori_idx]
    recoord = coords.copy()
    for i, c in enumerate(recoord):
        x,y = c
        recoord[i] = (x-ori[0], y-ori[1])
    hitdict = {}
    hitlist = []
    for i, coord in enumerate(recoord):
        x,y = coord
        hcf = compute_hcf(x,y)
        if hcf < 0:
            hcf = -hcf
        key = (x/hcf, y/hcf)
        hitlist.append(key) 
        if key in hitdict:
            hitdict[key].append((x,y, i))
        else:
            hitdict[key] = [(x,y, i)]

    for k, vs in hitdict.items():
        hitdict[k] = sorted(vs, key=lambda tup: tup[0]**2+tup[1]**2)

    rayslist = sorted(hitdict.keys(), key=lambda tup: clockwiseOrd((tup[0], tup[1])))
    cnt = 0
    for ray in cycle(rayslist):
        if hitdict[ray]:
            coord = hitdict[ray].pop(0)
            cnt += 1
            x = coord[0] + ori[0]
            y = coord[1] + ori[1]
            #print(f"{cnt}:{ray}={clockwiseOrd(ray)} | {(x,y)} | {hitdict[ray]}  ")
            if cnt == 200:
                x,y = coords[coord[2]]
                return 100*x+y



if __name__ == '__main__':
    fname = "input10.txt"
    _, xy, idx = part1(fname)
    print(part2(fname, xy, idx))

