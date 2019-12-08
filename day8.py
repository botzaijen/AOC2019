def readFileToDigits(filename):
    with open(filename,"r") as f:
        ds = list(f.readline().strip())
        return list(map(int, ds))

def part1():
    digs = readFileToDigits("input8.txt")
    lay = 25*6
    layers = len(digs) // lay
    result = []
    for li in range(layers):
        zeros = 0
        ones = 0
        twos = 0
        for di in range(lay):
            index = li*lay+di
            if digs[index] == 0:
                zeros += 1
            elif digs[index] == 1:
                ones += 1
            elif digs[index] == 2:
                twos += 1
        result.append((zeros, ones*twos))
    result.sort(key=lambda tup: tup[0])
    print(result)
    print(f"Answer: {result[0]}")

def part2():
    digs = readFileToDigits("input8.txt")
    cols = 25
    rows = 6
    layers = len(digs) // (cols*rows)
    result = []
    for yi in range(rows):
        print("")
        for xi in range(cols):
            for li in range(layers):
                index = li*(cols*rows)+yi*cols+xi
                if digs[index] != 2:
                    result.append(digs[index])
                    print(digs[index],end='')
                    break
    with open("day8.ppm","w") as f:
        f.write("P1\n")
        f.write(f"{cols} {rows}\n")
        for yi in range(rows):
            for xi in range(cols):
                f.write(f"{result[yi*cols+xi]} ")
            f.write("\n")





if __name__ == '__main__':
    #digs = readFileToDigits("input8.txt")
    #print(len(digs))
    #rows = len(digs) / 25
    #layers = rows / 6
    #print(f"Rows: {rows}, Layers: {layers}")
    part2()
