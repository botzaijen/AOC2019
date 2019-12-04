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

def isValid2(arr):
    predup = False
    dup = False
    dupdig = -1
    for i in range(1,len(arr)):
        if (arr[i-1] > arr[i]):
            return False
        if (arr[i-1] == arr[i]):
            if (arr[i] == dupdig):
                dup = False
            else:
                dup = True
                dupdig = arr[i]
        else:
            dupdig = -1
            if dup:
                predup = True
    return dup or predup

def part(validation_function):
    start, end = puzzle_input_arr
    okPassw = 0
    for passw in range(start, end+1):
        arr = splitToArray(passw)
        if validation_function(arr):
            okPassw = okPassw + 1
    print(f"Number of valid passwords in the range [{start}, {end}] = {okPassw}")


if __name__ == '__main__':
    #print(isValid(splitToArray(111111)))
    #print(isValid(splitToArray(223450)))
    #print(isValid(splitToArray(123789)))
    #print(isValid2(splitToArray(112233)))
    #print(isValid2(splitToArray(123444)))
    #print(isValid2(splitToArray(111122)))
    part(isValid2)

