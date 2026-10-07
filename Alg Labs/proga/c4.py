import sys
from collections import deque

v_count, e_count = map(int, sys.stdin.readline().split())

# Условие 1: в дереве должно быть V-1 рёбер
if e_count != v_count - 1:
    print("NO")
    sys.exit()

# Особые случаи
if v_count == 0:
    print("NO")  # пустой граф не считается деревом
    sys.exit()
if v_count == 1:
    print("YES")  # одна вершина без рёбер — дерево
    sys.exit()

# Строим список смежности
adj = [[] for _ in range(v_count)]
for _ in range(e_count):
    a, b = map(int, sys.stdin.readline().split())
    a -= 1
    b -= 1
    adj[a].append(b)
    adj[b].append(a)

# Проверяем связность с помощью BFS
visited = [False] * v_count
queue = deque([0])
visited[0] = True
count_visited = 1

while queue:
    v = queue.popleft()
    for neighbor in adj[v]:  # теперь правильно перебираем соседей
        if not visited[neighbor]:
            visited[neighbor] = True
            count_visited += 1
            queue.append(neighbor)

# Граф связен, если посетили все вершины
if count_visited == v_count:
    print("YES")
else:
    print("NO")