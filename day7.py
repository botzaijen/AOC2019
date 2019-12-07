from itertools import permutations
import math
from enum import Enum
class ProgramState(Enum):
    INIT = 0
    WAITING = 1
    HALTED = 2

class Program:
    def __init__(self, memory):
        self.mem = memory.copy()
        self.ip = 0
        self.state = ProgramState.INIT

    def run(self, inputs=[]):
        result = None
        while True:
            opcode, m1, m2, m3 = splitOpcode(self.mem[self.ip])
            if opcode == 1:
                self.mem[self.mem[self.ip+3]] = readParam(self.mem, m1, self.mem[self.ip+1]) + readParam(self.mem, m2, self.mem[self.ip+2])
                self.ip += 4
            elif opcode == 2:
                self.mem[self.mem[self.ip+3]] = readParam(self.mem, m1, self.mem[self.ip+1]) * readParam(self.mem, m2, self.mem[self.ip+2])
                self.ip += 4
            elif opcode == 3:
                if inputs:
                    inp = inputs.pop(0)
                else:
                    self.state = ProgramState.WAITING
                    return result
                addr = self.mem[self.ip+1]
                self.mem[addr] = inp
                self.ip += 2
            elif opcode == 4:
                param1 = readParam(self.mem, m1, self.mem[self.ip+1])
                print(f">>> {param1}")
                result = param1
                self.ip += 2
            elif opcode == 5: #jmp-if-true
                param1 = readParam(self.mem, m1, self.mem[self.ip+1])
                param2 = readParam(self.mem, m2, self.mem[self.ip+2])
                if param1 != 0:
                    self.ip = param2
                else:
                    self.ip += 3
            elif opcode == 6: #jmp-if-false
                param1 = readParam(self.mem, m1, self.mem[self.ip+1])
                param2 = readParam(self.mem, m2, self.mem[self.ip+2])
                if param1 == 0:
                    self.ip = param2
                else:
                    self.ip += 3
            elif opcode == 7: #less than
                param1 = readParam(self.mem, m1, self.mem[self.ip+1])
                param2 = readParam(self.mem, m2, self.mem[self.ip+2])
                addr = self.mem[self.ip+3]
                if param1 < param2:
                    self.mem[addr] = 1
                else:
                    self.mem[addr] = 0
                self.ip += 4
            elif opcode == 8: #equals
                param1 = readParam(self.mem, m1, self.mem[self.ip+1])
                param2 = readParam(self.mem, m2, self.mem[self.ip+2])
                addr = self.mem[self.ip+3]
                if param1 == param2:
                    self.mem[addr] = 1
                else:
                    self.mem[addr] = 0
                self.ip += 4
            elif opcode == 99:
                self.state = ProgramState.HALTED
                break
            else:
                print(f"Error interpreting opcode {opcode}")
                break
        return result


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
    return (op, mode1, mode2, mode3)

def readParam(mem, mode, val):
    if mode == 0: # position mode
        return mem[val]
    elif mode == 1: # immediate mode
        return val
    else:
        print(f"Error reading parameter {val}. Invalid mode {mode}")
        return None

def runProgram(memory, prn=False, inputs=[]):
    result = None
    ip = 0
    while True:
        opcode, m1, m2, m3 = splitOpcode(memory[ip])
        if prn:
            print(memory)
        if opcode == 1:
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}!{memory[ip+3]}")
            memory[memory[ip+3]] = readParam(memory, m1, memory[ip+1]) + readParam(memory, m2, memory[ip+2])
            ip = ip + 4
        elif opcode == 2:
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}!{memory[ip+3]}")
            memory[memory[ip+3]] = readParam(memory, m1, memory[ip+1]) * readParam(memory, m2, memory[ip+2])
            ip = ip + 4
        elif opcode == 3:
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}")
            if inputs:
                inp = inputs.pop(0)
            else:
                inp = input(">>> ")
            addr = memory[ip+1]
            memory[addr] = int(inp)
            ip = ip + 2
        elif opcode == 4:
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}")
            param1 = readParam(memory, m1, memory[ip+1])
            print(f">>> {param1}")
            result = param1
            ip = ip + 2
        elif opcode == 5: #jmp-if-true
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}")
            param1 = readParam(memory, m1, memory[ip+1])
            param2 = readParam(memory, m2, memory[ip+2])
            if param1 != 0:
                ip = param2
            else:
                ip = ip + 3
        elif opcode == 6: #jmp-if-false
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}")
            param1 = readParam(memory, m1, memory[ip+1])
            param2 = readParam(memory, m2, memory[ip+2])
            if param1 == 0:
                ip = param2
            else:
                ip = ip + 3
        elif opcode == 7: #less than
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}!{memory[ip+3]}")
            param1 = readParam(memory, m1, memory[ip+1])
            param2 = readParam(memory, m2, memory[ip+2])
            addr = memory[ip+3]
            if param1 < param2:
                memory[addr] = 1
            else:
                memory[addr] = 0
            ip = ip + 4
        elif opcode == 8: #equals
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}!{memory[ip+2]}!{memory[ip+3]}")
            param1 = readParam(memory, m1, memory[ip+1])
            param2 = readParam(memory, m2, memory[ip+2])
            addr = memory[ip+3]
            if param1 == param2:
                memory[addr] = 1
            else:
                memory[addr] = 0
            ip = ip + 4
        elif opcode == 99:
            if prn:
                print("Halt")
            break
        else:
            print(f"Error interpreting opcode {opcode}")
            break
    return result


def chainPrograms(mem, p):
    inputs = [p[0], 0]
    out = runProgram(mem.copy(), False, inputs)
    inputs = [p[1], out]
    out = runProgram(mem.copy(), False, inputs)
    inputs = [p[2], out]
    out = runProgram(mem.copy(), False, inputs)
    inputs = [p[3], out]
    out = runProgram(mem.copy(), False, inputs)
    inputs = [p[4], out]
    out = runProgram(mem.copy(), False, inputs)
    return out

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

def part1():
    memory = readFileToIntList("input7.txt")
    max_thrust = -math.inf
    for p in permutations([0,1,2,3,4]):
        mem = memory.copy()
        inputs = [p[0], 0]
        out = chainPrograms(mem, p)
        if out > max_thrust:
            max_thrust = out
    print(max_thrust)

def test():
    memory = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    print(chainPrograms(memory, [4,3,2,1,0]))
    memory = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
    print(chainPrograms(memory, [0,1,2,3,4]))
    memory = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    print(chainPrograms(memory, [1,0,4,3,2]))

def test2():
    memory = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    print(chainStatePrograms(memory, [9,8,7,6,5]))
    memory = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    print(chainStatePrograms(memory, [9,7,8,5,6]))

def part2():
    memory = readFileToIntList("input7.txt")
    max_thrust = -math.inf
    for p in permutations([5,6,7,8,9]):
        mem = memory.copy()
        out = chainStatePrograms(mem, p)
        if out > max_thrust:
            max_thrust = out
    print(max_thrust)


if __name__ == '__main__':
    part2()
