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
        self.rp = 0
        self.state = ProgramState.INIT

    def run(self, inputs=[]):
        result = None
        while True:
            opcode, m1, m2, m3 = splitOpcode(self.mem[self.ip])
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
                print(f">>> {param1}")
                result = param1
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
            self.pushMemIfIndexInvalid(val)
            return self.mem[val]
        elif mode == 1: # immediate mode
            return val
        elif mode == 2: # relative mode
            addr = self.rp+val
            self.pushMemIfIndexInvalid(addr)
            return self.mem[addr]
        else:
            print(f"Error reading parameter {val}. Invalid mode {mode}")
            return None

    def setParam(self, mode, val):
        if mode == 0: # position mode
            self.pushMemIfIndexInvalid(val)
            return val
        elif mode == 1: # immediate mode
            return val
        elif mode == 2: # relative mode
            addr = self.rp+val
            self.pushMemIfIndexInvalid(addr)
            return addr
        else:
            print(f"Error reading parameter {val}. Invalid mode {mode}")
            return None

    def pushMemIfIndexInvalid(self, addr):
        if addr >= len(self.mem):
            self.mem[len(self.mem):] = [0]*(addr-len(self.mem)+4)



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
    memory = readFileToIntList("input9.txt")
    print(Program(memory).run([1]))
def part2():
    memory = readFileToIntList("input9.txt")
    print(Program(memory).run([2]))


def test():
    memory = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    print(Program(memory).run())
    memory = [1102,34915192,34915192,7,4,7,99,0]
    print(Program(memory).run())
    memory = [104,1125899906842624,99]
    assert Program(memory).run() == 1125899906842624, "Should be 1125899906842624"


if __name__ == '__main__':
    part2()
