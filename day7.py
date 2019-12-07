from itertools import permutations
import math

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
    out = runProgram(mem, False, inputs)
    inputs = [p[1], out]
    out = runProgram(mem, False, inputs)
    inputs = [p[2], out]
    out = runProgram(mem, False, inputs)
    inputs = [p[3], out]
    out = runProgram(mem, False, inputs)
    inputs = [p[4], out]
    out = runProgram(mem, False, inputs)
    return out

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

if __name__ == '__main__':
    part1()
