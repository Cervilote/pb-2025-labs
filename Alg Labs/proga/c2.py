import array

v_count, e_count = map(int, input().split())

used_dfs = [False] * v_count

lst = [[] for i in range(v_count)]

for _ in range(e_count):
    a, b = map(int, input().split())
    a-=1
    b-=1

    lst[a].append(b)
    lst[b].append(a)

count=0

def dfs(v):
    stac = array.array('i', [v])
    while stac:
        ve = stac.pop()
        if not used_dfs[ve]:
            used_dfs[ve] = True
            stac.extend(i for i in lst[ve] if not used_dfs[i])

for v in range(v_count):
    if not used_dfs[v]:
        dfs(v)
        count += 1

print(count)
