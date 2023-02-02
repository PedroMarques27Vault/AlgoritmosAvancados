def f1(n):
    r=0
    for i in range(1,n+1):
        r+=i
    return r

def f2(n):
    r=0
    for i in range(1,n+1):
        for j in range(1,n+1):
            r+=1
    return r


def f3(n):
    r=0
    for i in range(1,n+1):
        for j in range(i,n+1):
            r+=1
    return r


def f4(n):
    r=0
    for i in range(1,n+1):
        for j in range(1,i+1):
            r+=j
    return r



def r1(n):
    if n== 0:
        return 0
    return 1+r1(n-1)



def r2(n):
    if n== 0:
        return 0
    if n==1:
        return 1
    return n+r2(n-2)
print(r2(5))