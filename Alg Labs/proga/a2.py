
def l(a,s,x):
    otv = -1
    c=0
    for i in range(s):
        c+=1
        if a[i] == x:
            otv=a[i]
            break
    return print(c)
def bi(a,s,x):
    c=0
    l, r = 0, s-1
    while l<=r:
        c += 1
        mid = (l + r) // 2
        if a[mid] == x:
            return print(c)
        elif a[mid] > x:
            r = mid-1
        else:
            l = mid+1
    return print(c)
s=int(input())
a=[int(i) for i in input().split()]
x=int(input())
l(a,s,x),bi(a,s,x)