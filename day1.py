def calcFuel(m):
    return (m // 3) -2

def calcFuelRec(m):
    fuel = (m // 3) -2
    if fuel <= 0:
        return 0
    else:
        return fuel + calcFuelRec(fuel)

def day1():
    with open("input1.txt", "r") as f:
        lines = f.readlines()
        masses = list(map(int, lines))
        s = sum(map(calcFuel, masses))
        s2 = sum(map(calcFuelRec, masses))
    print(f"part1: {s}")
    print(f"part2: {s2}")


if __name__ == '__main__':
    day1()
