# не ориентированный не взвешенный

v_count = int(input())
e_count = int(input())

# матрица смежности
mx = [[0] * v_count for _ in range(v_count)]
# списки смежности
lst = {i: [] for i in range(v_count)}
# список ребер
edges = []

for _ in range(e_count):
    a, b = map(int, input().split())

    mx[a][b] = mx[b][a] = 1

    lst[a].append(b)
    lst[b].append(a)

    edges.extend([(a, b), (b, a)])

for i in mx:
    print(*i)
print()
print(lst)
print()
print(edges)