input12 = [
      [-8, -9,  -7],
      [-5,  2,  -1],
      [11,  8, -14],
      [ 1, -4, -11],
      ]

testps = [
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]
]

testps2 = [
    [-8, -10, 0],
    [5, 5, 10],
    [2, -7, 3],
    [9, -8, -3],
]
from math import gcd

def simulate(no_steps, p, v=None, s=0):
    if v is None:
        v = [[0,0,0] for _ in p]
    for i in range(1, no_steps+1):
        v = updatevelocity(p, v)
        p = updateposition(p, v)
        s += 1
    return (p,v,s)

def updatevelocity(p, v):
    assert len(p) == len(v)
    newv = v.copy()
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            for ax in range(0,3):
                if p[i][ax] < p[j][ax]:
                    newv[i][ax] += 1
                    newv[j][ax] -= 1
                elif p[i][ax] > p[j][ax]:
                    newv[i][ax] -= 1
                    newv[j][ax] += 1
    return newv

def updateposition(p, v):
    assert len(p) == len(v)
    newp= p.copy()
    for i in range(len(p)):
        for ax in range(0,3):
            newp[i][ax] += v[i][ax]
    return newp

def calctotalenergy(p,v):
    E = 0
    for i in range(len(p)):
        P = 0
        K = 0
        for ax in range(0,3):
            P += abs(p[i][ax])
            K += abs(v[i][ax])
        E += P * K
    return E


def showpv(p,v,steps):
    energy = calctotalenergy(p,v)
    print(f"\nEnergy after {steps} steps: {energy}")
    for i in range(len(p)):
        x,y,z = p[i]
        vx,vy,vz = v[i]
        print(f"<pos=<x={x}, y={y}, z={z}>, vel=<x={vx}, y={vy}, z={vz}>")

def test1():
    p,v,s = simulate(1, testps)
    showpv(p,v,s)
    p,v,s = simulate(1, p,v,s)
    showpv(p,v,s)
    p,v,s = simulate(1, p,v,s)
    showpv(p,v,s)
    p,v,s = simulate(7, p,v,s)
    showpv(p,v,s)

def test2():
    p,v,s = simulate(100, testps2)
    showpv(p,v,s)

def part1():
    p,v,s = simulate(1000, input12)
    showpv(p,v,s)

def part2():
    #I did not come up with this solution on my own
    #according to u/jonathan_paulson the key insights to the problem are
    #1) axes are independent => you can find the period of each axis separately. 
    # the total period is then the least common multiple of these.
    #2) each axis will repeat quicker than the full cycle.
    #3) The system is completely reversible => each state has a unique parent => first 
    # repeat must be the starting state.

    p = input12
    v = [[0,0,0] for _ in p]
    state_set = {} 
    for ax in range(0,3):
        state_set[((p[0][ax], 0), (p[1][ax], 0), (p[2][ax], 0), (p[3][ax], 0))] = -1

    done = [False, False, False]
    s = 0
    while not all(done):
        v = updatevelocity(p, v)
        p = updateposition(p, v)
        s += 1
        for ax in range(0,3):
            if not done[ax]:
                h = ((p[0][ax], v[0][ax]), (p[1][ax], v[1][ax]), (p[2][ax], v[2][ax]), (p[3][ax], v[3][ax]))
                if h in state_set:
                    state_set[h] = s
                    done[ax] = True
                    print(f"{ax}: {s}")
    a = list(state_set.values())
    print(a)
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm*i//gcd(lcm,i)
    print(lcm)

if __name__ == '__main__':
    part2()
