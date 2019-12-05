
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

def runProgram(memory):
    ip = 0
    while True:
        opcode, m1, m2, m3 = splitOpcode(memory[ip])
        if opcode == 1:
            memory[memory[ip+3]] = readParam(memory, m1, memory[ip+1]) + readParam(memory, m2, memory[ip+2])
            ip = ip + 4
        elif opcode == 2:
            memory[memory[ip+3]] = readParam(memory, m1, memory[ip+1]) * readParam(memory, m2, memory[ip+2])
            ip = ip + 4
        elif opcode == 3:
            inp = input(">>> ")
            addr = memory[ip+1]
            memory[addr] = int(inp)
            ip = ip + 2
        elif opcode == 4:
            addr = memory[ip+1]
            print(f">>> {memory[addr]}")
            ip = ip + 2
        elif opcode == 99:
            break
        else:
            print(f"Error interpreting opcode {opcode}")
            break
    return memory

def part1():
    mem = readFileToIntList("input5.txt")
    mem = runProgram(mem)

if __name__ == '__main__':
    part1()
