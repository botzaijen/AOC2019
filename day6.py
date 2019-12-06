
def readFileToDict(filename):
    starmap = dict()
    with open(filename, "r") as f:
        codes = f.readlines()
        for c in codes:
            l = c.strip().split(')')
            key = l[0]
            val = l[1]
            if key in starmap:
                starmap[key].append(val)
            else:
                starmap[key] = [val]
    return starmap

def sumOrbits(sm, init_key, depth):
    if init_key not in sm:
        return depth
    childsum = 0
    for child in sm[init_key]:
        childsum += sumOrbits(sm, child, depth+1)
    return depth + childsum

def findLeaf(sm, init_key, search_key):
    if init_key not in sm:
        return None
    for child in sm[init_key]:
        if child == search_key:
            return [init_key]
        else:
            res = findLeaf(sm, child, search_key)
            if res is not None:
                res.append(init_key)
                return res
    return None


def part1():
    starmap = readFileToDict("input6.txt")
    orbsum = sumOrbits(starmap, 'COM', 0)
    print(orbsum)

def part2():
    starmap = readFileToDict("input6.txt")
    youcom = findLeaf(starmap, 'COM', 'YOU')
    sancom = findLeaf(starmap, 'COM', 'SAN')
    for i, p in enumerate(youcom, 0):
        if p in sancom:
            j = sancom.index(p)
            print(i+j)
            break


if __name__ == '__main__':
    part2()
    #starmap = readFileToDict('t61.txt')
    #orbsum = sumOrbits(starmap, 'COM', 0)
    #print(orbsum)
