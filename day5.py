
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

def runProgram(memory, prn=False):
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
            inp = input(">>> ")
            addr = memory[ip+1]
            memory[addr] = int(inp)
            ip = ip + 2
        elif opcode == 4:
            if prn:
                print(f"[{ip}]:{m3}|{m2}|{m1}|{opcode}|{memory[ip+1]}")
            param1 = readParam(memory, m1, memory[ip+1])
            print(f">>> {param1}")
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
    return memory

def part1():
    mem = readFileToIntList("input5.txt")
    mem = runProgram(mem, True)

def part2():
    mem = readFileToIntList("input5.txt")
    #mem = [3,9,8,9,10,9,4,9,99,-1,8]
    #mem = [3,9,7,9,10,9,4,9,99,-1,8]
    #mem = [3,3,1108,-1,8,3,4,3,99]
    #mem = [3,3,1107,-1,8,3,4,3,99]
    #mem = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    #mem = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    #mem = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    mem = runProgram(mem, False)
    #print(mem)

if __name__ == '__main__':
    part2()
