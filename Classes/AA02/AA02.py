def compute(a,b):
    value = a
    iter = 0
    for i in range(1,b):
        value=value*a
        iter+=1
    return value, iter

def recursiveCompute(a,b):
    if b == 0:
        return 1
    elif b == 1:
        return a
   
    return recursiveCompute(a,b//2)*recursiveCompute(a,(b+1)//2)
if __name__ == '__main__':
    print(compute(2,4))
    print(recursiveCompute(2,4))
