def can(max_s, a, k):
    si=1
    c=0
    for i in a:
        if c+i > max_s:
            si+=1
            c=i
        else:
            c+=i
    return si <= k
n,k=input().split(" ")
n=int(n)
k=int(k)
w = [int(i) for i in input().split()]
l = max(w)
r = sum(w)
while l < r:
    mid = (l + r) // 2
    if can(mid, w, k):
        r = mid
    else:
        l = mid + 1
print(l)