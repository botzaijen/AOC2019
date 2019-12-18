import math
from copy import deepcopy
from itertools import permutations
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
    #line = [str(x) for x in range(min_x,max_x+1)]
    #print(''.join(line))

    for y in range(min_y, max_y+1):
        line = [] #[str(y)]
        for x in range(min_x, max_x+1):
            pos = (x,y)
            line.append(display[pos])
        print(''.join(line))


class Vertex(object):
    def __init__(self, pos, tile):
        self.tile = tile
        self.pos = pos
        self.edges = [None, None, None, None]

    def add_adjecent(self,move_inst, response):
        idx = move_inst - 1
        x,y = self.pos
        if move_inst == 1:
            y += 1
        elif move_inst == 2:
            y -= 1
        elif move_inst == 3:
            x += 1
        elif move_inst == 4:
            x -= 1
        else: 
            print(f"Error illegal move_inst {move_inst}")
        adjpos = (x,y)
        tile = ' '
        if response == 0:
            tile = '#'
        elif response == 1:
            tile = '.'
        elif response == 2:
            tile = 'O'
        else: 
            print(f"Error illegal response {response}")
        self.edges[idx] = Vertex(adjpos, tile)
        return self.edges[idx]

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'Vertex(p='+str(self.pos)+', t='+str(self.tile)+', ['+str(self.edges)+'])'

def dirToPos(pos, move_inst):
    x,y = pos
    if move_inst == 1:
        y += 1
    elif move_inst == 2:
        y -= 1
    elif move_inst == 3:
        x -= 1
    elif move_inst == 4:
        x += 1
    else: 
        print(f"Error illegal move {move_inst}")
    return (x,y)

def get_adjecent(pos):
    return [dirToPos(pos,d) for d in [1,2,3,4]]

def back(move_inst):
    if move_inst == 1:
        return 2
    elif move_inst == 2:
        return 1
    elif move_inst == 3:
        return 4
    elif move_inst == 4:
        return 3
    else: 
        print(f"Error illegal move {move_inst}")
        return None



def part():
    memory = readFileToIntList("input15.txt")
    movemap = defaultdict(lambda: ' ') 
    prg = Program(memory)
    start_pos = (0,0)
    tile = '.'
    movemap[start_pos] = tile
    came_from = []
    move_cmd = {'north':1, 'south':2, 'west':3, 'east':4} 
    invmove_cmd = {v:k for k,v in move_cmd.items()} 
    def search_adj(start):
        stack = list(zip([1,2,3,4],get_adjecent(start)))
        while stack:
            move, pos = stack.pop()
            resp = prg.run([move])[0]
            print(f"attempting move {invmove_cmd[move]} to {pos}", end="")
            if resp == 0:
                movemap[pos] = '#'
                print(" found #, did not move")
            elif resp == 1:
                print(f" found {movemap[pos]}, new position {pos}")
                if movemap[pos] == '.':
                    movemap[pos] = 'x'
                else:
                    came_from.append(back(move))
                    movemap[pos] = '.'
                explored = True
                for mv, adj in enumerate(get_adjecent(pos), 1):
                    if movemap[adj] == ' ':
                        explored = False
                        stack.append((mv,adj))
                if explored:
                    print("backtracking...")
                    cam = came_from.pop()
                    adj = dirToPos(pos,cam)
                    stack.append((cam,adj))
            elif resp == 2:
                movemap[pos] = 'O'
                return pos
            else:
                print("Error")
        movemap[pos] = 'D'

    result = search_adj(start_pos)
    print(f"found oxygen at {result}")
    show(movemap)

if __name__ == '__main__':
    part()


