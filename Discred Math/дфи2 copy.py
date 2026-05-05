# O(n) - Линейный поиск
#  0 -1 2 9 4 7 8 9
# первый максимум - 9
# второй максимум - 8
k = int(input()),m= int(input())
a = [int(a) for a in input().split()]
max1, max2 = float('-inf'), float('-inf')
for i in a:
    if i > max1:
        max1, max2 = i, max1
    elif i > max2 and i != max1:
        max2 = i
print(a)