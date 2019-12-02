
def readFileToIntList(filename):
    with open(filename, "r") as f:
        codes = f.readline().split(',')
        intlist = list(map(int, codes))
    return intlist

def runProgram(memory):
    ip = 0
    while True:
        opcode = memory[ip]
        addr1 = memory[ip+1]
        addr2 = memory[ip+2]
        addr3 = memory[ip+3]
        if opcode == 1:
            memory[addr3] = memory[addr1] + memory[addr2]
            ip = ip + 4
        elif opcode == 2:
            memory[addr3] = memory[addr1] * memory[addr2]
            ip = ip + 4
        elif opcode == 99:
            break
        else:
            print(f"Error interpreting opcode {opcode}")
            break
    return memory

def printProgram(memory):
    ip = 0
    while True:
        opcode = memory[ip]
        addr1 = memory[ip+1]
        addr2 = memory[ip+2]
        addr3 = memory[ip+3]
        if opcode == 1:
            print(f"ADD [{addr1}]={memory[addr1]} [{addr2}]={memory[addr2]} => {addr3}")
            ip = ip + 4
        elif opcode == 2:
            print(f"MUL [{addr1}]={memory[addr1]} [{addr2}]={memory[addr2]} => {addr3}")
            ip = ip + 4
        elif opcode == 99:
            print("EXIT")
            break
        else:
            print(f"Error interpreting opcode {opcode}")
            break

def part1():
    mem = readFileToIntList("input2.txt")
    mem[1] = 12
    mem[2] = 2
    print(mem)
    mem = runProgram(mem)
    print(mem)
    print(f"Value at memory position 0: {mem[0]}")

def part2iterate(mem):
    for noun in range(0,100):
        for verb in range(0,100):
            inp = mem.copy()
            inp[1] = noun
            inp[2] = verb
            out = runProgram(inp)
            print(out[0])
            if out[0] == 19690720:
                return (noun, verb)
    return (-1,-1)

def part2():
    mem = readFileToIntList("input2.txt")
    noun, verb = part2iterate(mem)
    print(f"noun = {noun}, verb = {verb} => {100*noun+verb}")

    

if __name__ == '__main__':
    #part2()
    mem = readFileToIntList("input2.txt")
    printProgram(mem)
