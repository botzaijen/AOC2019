
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
        counts.append((c, ast))
        invc[ast] = c
    counts.sort(key=lambda tup: tup[0])
    print(counts[-1])


if __name__ == '__main__':
    part1("input10.txt")
