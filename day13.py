from itertools import permutations
import math
from enum import Enum
from collections import defaultdict

class ProgramState(Enum):
    INIT = 0
    WAITING = 1
    HALTED = 3



class Memory(object):
    def __init__(self, code):
        self.memory = {}
        for i, v in enumerate(code):
            self.memory[i] = v

    def __getitem__(self,key):
        assert key >= 0
        return self.memory.get(key, 0)

    def __setitem__(self, key, val):
        assert key >= 0
        self.memory[key] = val

class Program:
    def __init__(self, memory):
        self.mem = Memory(memory)
        self.ip = 0
        self.rp = 0
        self.state = ProgramState.INIT
        self.outputcalls = 0

    def run(self, inputs=[]):
        result = None
        while True:
            opcode, modes = splitOpcode(self.mem[self.ip])
            m1,m2,m3 = modes
            if opcode == 1:
                addr = self.mem[self.ip+3]
                self.mem[self.setParam(m3, addr)] = self.readParam(m1, self.mem[self.ip+1]) + self.readParam(m2, self.mem[self.ip+2])
                self.ip += 4
            elif opcode == 2:
                addr = self.mem[self.ip+3]
                self.mem[self.setParam(m3, addr)] = self.readParam( m1, self.mem[self.ip+1]) * self.readParam( m2, self.mem[self.ip+2])
                self.ip += 4
            elif opcode == 3:
                if inputs:
                    inp = inputs.pop(0)
                else:
                    self.state = ProgramState.WAITING
                    return result
                addr = self.setParam(m1, self.mem[self.ip+1])
                self.mem[addr] = inp
                self.ip += 2
            elif opcode == 4:
                param1 = self.readParam( m1, self.mem[self.ip+1])
                if not result:
                    result = [param1]
                    #print(f"Col: {param1}")
                    self.outputcalls += 1
                else: 
                    result.append(param1)
                    #print(f"Dir: {param1}")
                self.ip += 2
            elif opcode == 5: #jmp-if-true
                param1 = self.readParam( m1, self.mem[self.ip+1])
                param2 = self.readParam( m2, self.mem[self.ip+2])
                if param1 != 0:
                    self.ip = param2
                else:
                    self.ip += 3
            elif opcode == 6: #jmp-if-false
                param1 = self.readParam( m1, self.mem[self.ip+1])
                param2 = self.readParam( m2, self.mem[self.ip+2])
                if param1 == 0:
                    self.ip = param2
                else:
                    self.ip += 3
            elif opcode == 7: #less than
                param1 = self.readParam( m1, self.mem[self.ip+1])
                param2 = self.readParam( m2, self.mem[self.ip+2])
                addr = self.setParam(m3, self.mem[self.ip+3])
                if param1 < param2:
                    self.mem[addr] = 1
                else:
                    self.mem[addr] = 0
                self.ip += 4
            elif opcode == 8: #equals
                param1 = self.readParam( m1, self.mem[self.ip+1])
                param2 = self.readParam( m2, self.mem[self.ip+2])
                addr = self.setParam(m3, self.mem[self.ip+3])
                if param1 == param2:
                    self.mem[addr] = 1
                else:
                    self.mem[addr] = 0
                self.ip += 4
            elif opcode == 9:
                param1 = self.readParam( m1, self.mem[self.ip+1])
                self.rp += param1
                self.ip += 2
            elif opcode == 99:
                self.state = ProgramState.HALTED
                break
            else:
                print(f"Error interpreting opcode {opcode}")
                break
        return result


    def readParam(self, mode, val):
        if mode == 0: # position mode
            return self.mem[val]
        elif mode == 1: # immediate mode
            return val
        elif mode == 2: # relative mode
            addr = self.rp+val
            return self.mem[addr]
        else:
            print(f"Error reading parameter {val}. Invalid mode {mode}")
            return None

    def setParam(self, mode, val):
        if mode == 0: # position mode
            return val
        elif mode == 1: # immediate mode
            return val
        elif mode == 2: # relative mode
            addr = self.rp+val
            return addr
        else:
            print(f"Error reading parameter {val}. Invalid mode {mode}")
            return None



def readFileToIntList(filename):
    with open(filename, "r") as f:
        codes = f.readline().split(',')
        intlist = list(map(int, codes))
    return intlist

def splitOpcode(code):
    op = code % 100
    mode1 = (code // 100) % 10
    mode2 = (code // 1000) % 10
    mode3 = (code // 10000) % 10
    return (op, [mode1, mode2, mode3])

def show(display):
    xs = [x for x, _ in display.keys()]
    ys = [y for _, y in display.keys()]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            pos = (x,y)
            if x == -1:
                continue
            c = display[pos]
            if c == 0:
                line.append(' ');
            elif c == 1:
                line.append('+');
            elif c == 2:
                line.append('#');
            elif c == 3:
                line.append('=');
            elif c == 4:
                line.append('O');
            else:
                assert 'Unknown color', c
        print(''.join(line))

def part1():
    memory = readFileToIntList("input13.txt")
    prg = Program(memory)
    out = prg.run([])
    display = defaultdict(lambda: []) 
    for idx in range(0,len(out),3):
        x=out[idx]
        y=out[idx+1]
        tileid=out[idx+2]
        display[(x,y)].append(tileid)
    #print(len(display.keys()))
    #maxx = sorted(display.keys(), key=lambda tup: tup[0])
    #maxy = sorted(display.keys(), key=lambda tup: tup[1])
    #print(f"x: {maxx[0]}-{maxx[-1]}, y: {maxy[0]}-{maxy[-1]}")
    show(display)
    blocks = sum(1 for v in display.values() if v == 2)
    print(blocks)

def part2():
    memory = readFileToIntList("input13.txt")
    memory[0] = 2
    prg = Program(memory)
    #out = prg.run([])
    display = defaultdict(lambda: None) 
    inp = []
    out = prg.run(inp)
    for idx in range(0,len(out),3):
        x=out[idx]
        y=out[idx+1]
        tileid=out[idx+2]
        display[(x,y)] = tileid
    blocks = sum(1 for v in display.values() if v == 2)

    inp = [0]
    while True:
        out = prg.run(inp)
        ballp = -1
        paddlep = -1
        for idx in range(0,len(out),3):
            x=out[idx]
            y=out[idx+1]
            tileid=out[idx+2]
            old_tileid=display[(x,y)]
            display[(x,y)] = tileid
            if x >= 0:
                if old_tileid == 2 and tileid == 0:
                    blocks -= 1
                elif tileid == 4:
                    ballp = x
                elif tileid == 3:
                    paddlep = x
        print(f"blocks: {blocks}")
        if blocks == 0:
            break
        elif ballp < paddlep:
            inp = [-1]
        elif ballp > paddlep:
            inp = [1]
        else:
            inp = [0]
    score = display[(-1,0)]
    print(score)
    show(display)

if __name__ == '__main__':
    part2()
