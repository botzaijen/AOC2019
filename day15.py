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


class Vertex(object):
    def __init__(self, pos, tile):
        self.tile = tile
        self.pos = pos
        self.edges = [None, None, None, None]

    def add_adjecent(self,move_inst, response):
        idx = move_inst - 1
        x,y = self.pos
        if move_inst == move_cmd['north']:
            y -= 1
        elif move_inst == move_cmd['south']:
            y += 1
        elif move_inst == move_cmd['west']:
            x += 1
        elif move_inst == move_cmd['east']:
            x -= 1
        else: 
            print("Error illegal move_inst")
        adjpos = (x,y)
        if response == 0:
            tile = '#'
        elif response == 1:
            tile = '.'
        elif response == 2:
            tile = 'O'
        else: 
            print("Error illegal response")
        self.edges[idx] = Vertex(adjpos, tile)
        return self.edges[idx]

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'Vertex(p='+str(self.pos)+', t='+str(self.tile)+', ['+str(self.edges)+'])'

def part():
    memory = readFileToIntList("input15.txt")
    movemap = {} 
    prg = Program(memory)
    pos = (0,0)
    tile = '.'
    movemap[pos] = tile
    move_cmd = {'north':1, 'south':2, 'west':3, 'east':4} 
    start = Vertex(pos, tile)
    def search_adj(vert):
        for mv, adj in enumerate(1,vert.edges):
            if adj is None:
                resp = prg.run([mv])
                neigh = vert.add_adjecent(mv,resp)
                movemap[neigh.pos] = neigh.tile
                if resp == 1:
                    search_adj(neigh)
                elif resp == 2:
                    return neigh.pos







def get_topological_order(graph, startname):
    topo_order = []
    visited = set()

    def toposort(vertex, name):
        if not vertex.edges: # the vertex has no outgoing edges
            topo_order.append(name)
            return
        for childname in vertex.edges:
            if childname in visited:
                continue
            visited.add(childname)
            toposort(graph[childname], childname)
        topo_order.append(name)
    
    toposort(graph[startname], startname)
    return topo_order

def part1(graph):
    order = get_topological_order(graph, "FUEL")
    order.reverse()
    for name in order:
        vertex = graph[name]
        if vertex.rxn_produced == 0:
            print(name + str(vertex))
        its = max(1, math.ceil(vertex.required / vertex.rxn_produced))
        for reactant_name, cost in vertex.edges.items():
            graph[reactant_name].required += its*cost
    return graph["ORE"].required

if __name__ == '__main__':


