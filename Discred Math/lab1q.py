# Вход: a – упорядоченный по возрастанию список,
# x – число
# Выход: индекс наибольшего элемента i:
# a[i] <= x или -1, если такого индекса нет
from binascii import a2b_base64


def sol_anecdotes(n):
    # место для вашего решения
    a=[(1, 2), (3, 4), (1, 3), (2, 4)]
    s=n-4
    if n == 4:
        return [(1, 2), (3, 4), (1, 3), (2, 4)]
    else:
        if n>4:
            while s>0:
                s=s-1
                [(1+s,s)]+a
            return print(a)
    

a = [1,2,3,4,5,6]
x = 3
a1= [1,2,2,2,2,3,4,5]
x1=3
a2=[1,2,3,3,3,3,4,5]
x2=3
a3=[-2,-1,0,1,2,3,4]
x3=3
a4=[1,2,4,5,6,7]
x4=9
a5=[-3,-2,-1,1,2,3,4,5,6]
x5=-1
a6=[1,2,3,4,5]
x6=-2
a7=[1,1.2,1.5,2.1,4,3*2]
x7=3
print('1a=',a,'x=',x,':',upper_bound(a, x))
print('2a=',a1,'x=',x1,':',upper_bound(a1, x1))
print('3a=',a2,'x=',x2,':',upper_bound(a2, x2))
print('4a=',a3,'x=',x3,':',upper_bound(a3, x3))
print('5a=',a4,'x=',x4,':',upper_bound(a4, x4))
print('6a=',a5,'x=',x5,':',upper_bound(a5, x5))
print('7a=',a6,'x=',x6,':',upper_bound(a6, x6))
print('8a=',a7,'x=',x7,':',upper_bound(a7, x7))
