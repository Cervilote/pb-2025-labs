s,d=input().split(" ")
s=int(s)
d=int(d)
a = [int(i) for i in input().split()]
for i in range(s):
    if a[i] == d:
        otv=i+1
        break
    else:
        otv=-1
print(otv)
