def grasshopper_ways(n):
    mod = 10**9 + 7
    if n == 1:
        return 1
    if n == 2:
        return 1
    a,b=1,1
    for _ in range(3,n+1):
        a,b=b,(a+b) % mod
    return b
print(grasshopper_ways(int(input())))
