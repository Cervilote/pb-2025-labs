INF = float('inf')


def fmt(x):
    if x == INF:
        return "INF"
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return str(x)


def print_matrix(title, matrix, row_names, col_names):
    print(title)
    width = max(4, max(len(name) for name in list(row_names) + list(col_names) + [fmt(x) for row in matrix for x in row]))
    header = " " * width + " ".join(name.rjust(width) for name in col_names)
    print(header)
    for name, row in zip(row_names, matrix):
        print(name.rjust(width) + " ".join(fmt(x).rjust(width) for x in row))
    print()


n = int(input("Количество вершин: "))
names = input("Имена вершин через пробел (например A B C D): ").split()
print(f"Введите матрицу смежности {n}x{n} (0 — нет ребра, число — вес/наличие ребра):")
A = []
for i in range(n):
    A.append(list(map(int, input().split())))

print()
print("Введённая матрица смежности:")
print_matrix("Матрица смежности:", A, names, names)

edges = []
for i in range(n):
    for j in range(i + 1, n):
        if A[i][j] != 0:
            edges.append((i, j))

m = len(edges)
edge_names = [f"e{k}" for k in range(1, m + 1)]

print("Обозначение рёбер:")
for k, (i, j) in enumerate(edges, 1):
    print(f"e{k}: {names[i]}-{names[j]}")
print()

incidence = [[0] * m for _ in range(n)]
oriented = [[0] * m for _ in range(n)]
for k, (i, j) in enumerate(edges):
    incidence[i][k] = 1
    incidence[j][k] = 1
    oriented[i][k] = 1
    oriented[j][k] = -1

print_matrix("Матрица инцидентности (строки — вершины, столбцы — рёбра):", incidence, names, edge_names)

kirchhoff = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        s = 0
        for k in range(m):
            s += oriented[i][k] * oriented[j][k]
        kirchhoff[i][j] = s

print("Матрица Кирхгофа получена из матрицы инцидентности: L = B * B^T")
print("(B — ориентированная матрица инцидентности: +1 и -1 на концах ребра)")
print_matrix("Матрица Кирхгофа:", kirchhoff, names, names)

dist = [[INF] * n for _ in range(n)]
for i in range(n):
    dist[i][i] = 0
    for j in range(n):
        if i != j and A[i][j] != 0:
            dist[i][j] = A[i][j]

for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

print_matrix("Матрица расстояний:", dist, names, names)

print("Эксцентриситеты вершин:")
eccs = []
for i in range(n):
    ecc = max(dist[i])
    eccs.append(ecc)
    print(f"e({names[i]}) = {fmt(ecc)}")

finite = [e for e in eccs if e != INF]
if finite:
    radius = min(finite)
    print("Радиус графа:", fmt(radius))
else:
    print("Радиус графа: INF")
print()

start = input("Кратчайший путь ОТ вершины (например A): ").strip()
end = input("Кратчайший путь ДО вершины (например E): ").strip()
if start not in names:
    print(f"Вершины {start} нет в графе")
elif end not in names:
    print(f"Вершины {end} нет в графе")
else:
    i = names.index(start)
    j = names.index(end)
    print(f"Длина кратчайшего пути {start} — {end}: {fmt(dist[i][j])}")