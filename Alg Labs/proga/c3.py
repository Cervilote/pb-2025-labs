from collections import deque
with open('input.txt', 'r') as infile:
    v_count, e_count = map(int, infile.readline().split())
    if e_count > v_count - 1:
        with open('output.txt', 'w') as outfile:
            outfile.write("NO")
            exit()
    lst = [[] for _ in range(v_count)]

    for _ in range(e_count):
        a, b = map(int, infile.readline().split())
        a -= 1
        b -= 1
        lst[a].append(b)
        lst[b].append(a)



visited = [False] * v_count
queue = deque([0])
visited[0] = True
count = 1

while queue:
    v = queue.popleft()
    for ve in lst[v]:
        if not visited[ve]:
            visited[ve] = True
            count += 1
            queue.append(ve)

ss = count == v_count

with open('output.txt', 'w') as outfile:
    if ss:
        outfile.write("YES")
    else:
        outfile.write("NO")
