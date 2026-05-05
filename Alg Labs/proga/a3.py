s,d=input().split(" ")
s=int(s)
d=int(d)
a = [int(i) for i in input().split()]
l, r = -1, s
while r - l > 1:
    mid = (l + r) // 2
    if a[mid] >= d:
        r = mid
    else:
        l = mid

if r == s:
    print(-1)
else:
    print(a[r])
