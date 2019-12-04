puzzle_input_arr = (158126, 624574)

def splitToArray(num):
    #assert num >= 100000 <=10000000
    str_num = str(num)
    arr = list(map(int,str_num))
    return arr

def isValid(arr):
    dup = False
    for i in range(1,len(arr)):
        if (arr[i-1] > arr[i]):
            return False
        if (arr[i-1] == arr[i]):
            dup = True
    return dup

def part1():
    start, end = puzzle_input_arr
    okPassw = 0
    for passw in range(start, end+1):
        arr = splitToArray(passw)
        if isValid(arr):
            okPassw = okPassw + 1
    print(f"Number of valid passwords in the range [{start}, {end}] = {okPassw}")


if __name__ == '__main__':
    #print(isValid(splitToArray(111111)))
    #print(isValid(splitToArray(223450)))
    #print(isValid(splitToArray(123789)))
    part1()

