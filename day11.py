from itertools import permutations
import math
from enum import Enum
from collections import defaultdict

class ProgramState(Enum):
    INIT = 0
    WAITING = 1
    HALTED = 3

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Robot:
    def __init__(self, intcode):
        self.facing = Direction.UP
        self.x = 0
        self.y = 0
        self.map = defaultdict(lambda: 0)
        self.program = Program(intcode)
        self.painted = set()

    def turn(self, dircode):
        if dircode != 0 and dircode != 1:
            print(f"Error illegal turn direction {dircode}")
            return
        if self.facing == Direction.UP:
            if dircode == 0:
                self.facing = Direction.LEFT
            else:
                self.facing = Direction.RIGHT
        elif self.facing == Direction.RIGHT:
            if dircode == 0:
                self.facing = Direction.UP
            else:
                self.facing = Direction.DOWN
        elif self.facing == Direction.DOWN:
            if dircode == 0:
                self.facing = Direction.RIGHT
            else:
                self.facing = Direction.LEFT
        elif self.facing == Direction.LEFT:
            if dircode == 0:
                self.facing = Direction.DOWN
            else:
                self.facing = Direction.UP

    def move(self, dircode):
        dirstr = lambda d: 'LEFT' if d == 0 else 'RIGHT' 
        self.turn(dircode)
        if self.facing == Direction.UP:
            self.y -= 1
        elif self.facing == Direction.RIGHT:
            self.x += 1
        elif self.facing == Direction.DOWN:
            self.y += 1
        elif self.facing == Direction.LEFT:
            self.x -= 1


    def readtile(self):
        return self.map[(self.x, self.y)]

    def paint(self, colcode):
        self.map[(self.x, self.y)] = colcode # 0 = BLACK 1 = WHITE
        self.painted.add((self.x, self.y))

    def run(self):
        instructions = [0,0,0]
        while self.program.state != ProgramState.HALTED:
            tilecol = self.readtile()
            instructions = self.program.run([tilecol])
            if instructions:
                colcode = instructions[0]
                dircode = instructions[1]
                self.paint(colcode)
                self.move(dircode)
            else:
                print(self.program.state)

def show(travel_map):
    xs = [x for x, _ in travel_map.keys()]
    ys = [y for _, y in travel_map.keys()]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            pos = (x,y)
            c = travel_map[pos]
            if c == 0:
                line.append(' ');
            elif c == 1:
                line.append('#');
            else:
                assert 'Unknown color', c
        print(''.join(line))

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


def chainStatePrograms(mem, p):
    prgs = [Program(mem), Program(mem), Program(mem), Program(mem), Program(mem)] 
    done = False
    last_input = 0
    while not done:
        for i, prg in enumerate(prgs):
            if prg.state == ProgramState.INIT:
                inputs = [p[i], last_input]
            else:
                inputs = [last_input]
            out = prg.run(inputs)
            if prg.state == ProgramState.HALTED:
                done = True
            last_input = out
    return last_input

def part(starttilecol=0):
    memory = readFileToIntList("input11.txt")
    robot = Robot(memory)
    robot.map[(0,0)] = starttilecol
    robot.run()
    print(f"Number of tiles painted = {len(robot.painted)}")

    ll = list(zip(*robot.map.keys()))
    xs = list(ll[0])
    ys = list(ll[1])
    print(f"x: {min(xs)} - {max(xs)}")
    print(f"y: {min(ys)} - {max(ys)}")
    show(robot.map)


if __name__ == '__main__':
    part(0)
    part(1)
