N,A,B=input().split(" ")
N=int(N)
A=int(A)
B=int(B)
def F(x):
    return x * (A - B * x)
l, r = 1, N
while r-l > 2:
    m1 = l+(r-l)//3
    m2 = r-(r-l)//3
    if F(m1) < F(m2):
        l = m1
    else:
        r = m2
fin = max(F(x) for x in range(l,r+1))
print(fin)
