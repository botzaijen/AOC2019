def getNewPoint(start, stepstr):
    direction = stepstr[0]
    val = int(stepstr[1:])
    x,y = start
    if direction == 'U':
        return (x,y+val)
    elif direction == 'D':
        return (x,y-val)
    elif direction == 'R':
        return (x+val, y)
    else: 
        return (x-val, y)

def readFileToPointLists(filename):
    with open(filename, "r") as f:
        fst = f.readline().strip().split(',')
        ori = (0,0)
        p1 = [ori]
        o = ori
        for s in fst:
            n = getNewPoint(o, s)
            p1.append(n)
            o = n
            
        snd = f.readline().strip().split(',')
        p2 = [ori]
        o = ori
        for s in snd:
            n = getNewPoint(o, s)
            p2.append(n)
            o = n
    return (p1, p2)

def readFileToPointDistLists(filename):
    with open(filename, "r") as f:
        fst = f.readline().strip().split(',')
        ori = (0,0)
        p1 = [(0,0,0)]
        o = ori
        d = 0
        for s in fst:
            x,y = getNewPoint(o, s)
            d = d + abs(x-o[0]) + abs(y-o[0])
            p1.append((x,y,d))
            o = (x,y)
            
        snd = f.readline().strip().split(',')
        p2 = [(0,0,0)]
        o = ori
        d = 0
        for s in snd:
            x,y = getNewPoint(o, s)
            d = d + abs(x-o[0]) + abs(y-o[0])
            p2.append((x,y,d))
            o = (x,y)
    return (p1, p2)

def lineIsHorizontal(line):
    pa1, pa2 = line
    _, ya1 = pa1
    _, ya2 = pa2
    if ya1 == ya2:
        return True
    else:
        return False

def linesCrossing(line_a, line_b):
    ha = lineIsHorizontal(line_a)
    hb = lineIsHorizontal(line_b)
    if (ha and hb): # lines are parallel and can't cross
        return None
    elif ((not ha) and (not hb)): # lines are parallel and can't cross
        return None

    pa1, pa2 = line_a
    pb1, pb2 = line_b
    xa1, ya1 = pa1
    xa2, ya2 = pa2
    xb1, yb1 = pb1
    xb2, yb2 = pb2

    if ha:
        axmin = min(xa1, xa2)
        axmax = max(xa1, xa2)
        bymin = min(yb1, yb2)
        bymax = max(yb1, yb2)
        if (axmin <= xb1 and xb1 <= axmax) and (bymin <= ya1 and ya1 <= bymax):
            return (xb1, ya1)
        else:
            return None
    else:
        aymin = min(ya1, ya2)
        aymax = max(ya1, ya2)
        bxmin = min(xb1, xb2)
        bxmax = max(xb1, xb2)
        if (aymin <= yb1 and yb1 <= aymax) and (bxmin <= xa1 and xa1 <= bxmax):
            return (xa1, yb1)
        else:
            return None

def naivePart1():
    fst, snd = readFileToPointLists("input3.txt")
    hits = []
    for i in range(1,len(fst)):
        line_a = (fst[i-1], fst[i])
        for j in range(1,len(snd)):
            line_b = (snd[j-1], snd[j])
            cross = linesCrossing(line_a, line_b)
            if cross:
                hits.append(abs(cross[0])+abs(cross[1]))

    hits.sort()
    print(hits)

def naivePart2():
    fst, snd = readFileToPointDistLists("t1.txt")
    dists = []
    for i in range(1,len(fst)):
        xa1,ya1,da1 = fst[i-1]
        xa2,ya2,da2 = fst[i]
        line_a = ((xa1, ya1), (xa2, ya2))
        for j in range(1,len(snd)):
            xb1,yb1,db1 = snd[j-1]
            xb2,yb2,db2 = snd[j]
            line_b = ((xb1, yb1), (xb2, yb2))
            cross = linesCrossing(line_a, line_b)
            if cross:
                da = da1 + abs(cross[0]-xa1) + abs(cross[1]-ya1)
                db = db1 + abs(cross[0]-xb1) + abs(cross[1]-yb1)
                dists.append(da+db)

    dists.sort()
    print(dists)

if __name__ == '__main__':
    naivePart2()
