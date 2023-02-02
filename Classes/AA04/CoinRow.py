coins = [1,5,10,15,20,25]

def coinRowProblem(numberOfCoins):
    n = numberOfCoins-1
    print("Coin n: " + str(numberOfCoins))
    if numberOfCoins == 0:
        return 0
    elif numberOfCoins == 1:
        print(coins[0])
        return coins[0]
    if 1<n and n<len(coins):
        a = coins[n]
        print("A: "+ str(a))
        b = coinRowProblem(numberOfCoins-2)
        c = coinRowProblem(numberOfCoins-1)
  
        print(b)
        print(str(numberOfCoins) + " - " +c)
        return a+b+c

print(coinRowProblem(6))