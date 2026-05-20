v_count, e_count = map(int, input().split())

lst = {i: [] for i in range(v_count)}

for _ in range(e_count):
    a, b = map(int, input().split())
    lst[a-1].append(b-1)
    lst[b-1].append(a-1)

print(lst)

used_dfs = [False] * v_count
coun=0
def dfs(v):
    used_dfs[v] = True
    coun=+1

    for e in lst[v]:
        if not used_dfs[e]:
            dfs(e)
dfs(0)
print(used_dfs)
print(coun)