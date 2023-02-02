import time
table = {}
def fib(n):
    if n== 0 or n == 1:
        return n
    if n in table.keys():
        return table[n]
    else: 
        result = fib(n-1) + fib(n-2)
        table[n] = result
        return result

def normalFib(n):
    if n== 0 or n == 1:
        return n
    return normalFib(n-1) + normalFib(n-2)

t = time.time()
print(fib(20))
t2 = time.time()
print("Execution time " + str(t2-t))

t = time.time()
print(normalFib(20))
t2 = time.time()
print("Execution time " + str(t2-t))