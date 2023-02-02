matrix = []

previousData = {}
def D(m,n):
    if m== 0 or n== 0:
        return 1
    
    a = 0
    b = 0
    c = 0
    if (m-1,n) in previousData:
        a = previousData[(m-1,n)]
    else:
        a = D(m-1,n)
    if (m-1,n-1) in previousData:
        b = previousData[(m-1,n-1)]
    else:
        b = D(m-1,n-1)
    if (m,n-1) in previousData:
        c = previousData[(m,n-1)]
    else:
        c = D(m, n-1)
    return a+b+c

def DMatrix2D(m,n):
    matrix = [[None]*(n+1) for i in range(m+1) ]

   
    
    
    for i in range(0,m+1):
        for j in range(0,n+1):
            if i == 0 or j== 0:
                matrix[i][j]=1
            else:
                matrix[i][j] = matrix[i-1][j] + matrix[i-1][j-1] + matrix[i][j-1]

    for i in range(m+1):
        print(matrix[i])
    return matrix[m][n]
print(D(3,3))
print(DMatrix2D(3,3))