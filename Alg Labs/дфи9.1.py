"""
Лабораторная работа №9
Система маршрутизации курьерской службы
Графы, BFS, кратчайший путь

"""

from collections import deque

# ─── Исходные данные ─────────────────────────────────────────────
vertices = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'F')]


# ══════════════════════════════════════════════════════════════════
#  ЗАДАНИЕ 1 — Построение и отображение графа
# ══════════════════════════════════════════════════════════════════

# --- 1.1  Матрица смежности ----------------------------------------

def build_adjacency_matrix(edges, vertices):
    """
    Строит матрицу смежности (вложенный список n×n).
    Сложность: O(V² + E)
      - O(V²) — создание нулевой матрицы
      - O(E)  — заполнение единиц по рёбрам
    """
    n = len(vertices)
    # Словарь для быстрого поиска индекса вершины: {'A': 0, 'B': 1, ...}
    idx = {v: i for i, v in enumerate(vertices)}

    # Создаём нулевую матрицу n×n
    matrix = [[0] * n for _ in range(n)]

    # Для каждого ребра ставим 1 в обе стороны (граф неориентированный)
    for u, v in edges:
        i, j = idx[u], idx[v]
        matrix[i][j] = 1
        matrix[j][i] = 1

    return matrix


def print_matrix(matrix, vertices):
    """Красиво выводит матрицу с метками."""
    header = "     " + "  ".join(vertices)
    print(header)
    for i, row in enumerate(matrix):
        print(f"  {vertices[i]}  [" + ", ".join(str(x) for x in row) + "]")


# --- 1.2  Список смежности ----------------------------------------

def build_adjacency_list(edges, vertices):
    """
    Строит список смежности (словарь {вершина: [соседи]}).
    Сложность: O(V + E)
      - O(V) — создание пустых списков
      - O(E) — добавление соседей
    """
    graph = {v: [] for v in vertices}

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    return graph


# --- 1.3  Степень вершины ------------------------------------------

def degree(graph: dict, vertex: str) -> int:
    """
    Возвращает степень вершины (кол-во соседей).
    Сложность: O(1) — len() для списка в Python работает за O(1).
    """
    return len(graph[vertex])


# --- 1.4  Проверка теоремы Эйлера (Handshaking Lemma) -------------

def check_euler(graph: dict, edges: list) -> bool:
    """
    Сумма степеней всех вершин == 2 * кол-во рёбер.
    Сложность: O(V) — проход по всем вершинам.
    """
    sum_degrees = sum(degree(graph, v) for v in graph)
    double_edges = 2 * len(edges)

    print(f"  Сумма степеней: {sum_degrees}")
    print(f"  2 × рёбер:     {double_edges}")

    if sum_degrees == double_edges:
        print("Граф корректен")
        return True
    else:
        print("Граф НЕ корректен!")
        return False



#  ЗАДАНИЕ 2 — BFS: кратчайший путь и расстояния


# 2.1  Обход графа (BFS)

def bfs(graph: dict, start: str) -> list:
    """
    Обход в ширину. Возвращает список вершин в порядке посещения.

    Ключевая идея:
      - Используем очередь (deque) — добавляем в конец, забираем из начала.
      - Множество visited — чтобы не заходить в вершину дважды.

    Сложность: O(V + E)
      - Каждая вершина добавляется в очередь ровно 1 раз  → O(V)
      - Каждое ребро просматривается ровно 2 раза (с каждого конца) → O(E)
    """
    visited = set()        # Множество посещённых вершин
    queue = deque([start]) # Очередь: начинаем со стартовой вершины
    visited.add(start)
    order = []             # Порядок обхода

    while queue:
        # Извлекаем первую вершину из очереди (FIFO)
        current = queue.popleft()
        order.append(current)

        # Перебираем всех соседей текущей вершины
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


# 2.2  Расстояния от стартовой вершины

def bfs_distances(graph: dict, start: str) -> dict:
    """
    Возвращает {вершина: расстояние} от start до каждой достижимой вершины.

    Расстояние — кол-во рёбер (пересадок).

    Сложность: O(V + E) — тот же BFS, просто сохраняем расстояние.
    """
    distances = {start: 0}
    queue = deque([start])

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in distances:  # ещё не посещён
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


# --- 2.3  Кратчайший путь ------------------------------------------

def bfs_shortest_path(graph: dict, start: str, end: str) -> list | None:
    """
    Возвращает кратчайший путь [start, ..., end] или None.

    Идея: при BFS запоминаем для каждой вершины её «предка» —
    вершину, из которой мы впервые в неё пришли.
    Потом восстанавливаем путь от end к start по цепочке предков.

    Сложность:
      Лучший:  O(1)    — start == end
      Средний: O(V+E)  — стандартный BFS
      Худший:  O(V+E)  — end — самая дальняя вершина или недостижима
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([start])
    predecessors = {start: None}  # Словарь предков

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                predecessors[neighbor] = current  # Запоминаем: пришли из current
                queue.append(neighbor)

                # Нашли цель — сразу восстанавливаем путь
                if neighbor == end:
                    path = []
                    node = end
                    while node is not None:
                        path.append(node)
                        node = predecessors[node]
                    path.reverse()
                    return path

    return None  # Путь не найден (вершины в разных компонентах)



#  ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ — Компоненты связности


def find_connected_components(graph: dict) -> list[list]:
    """
    Находит все компоненты связности графа.

    Идея: запускаем BFS из каждой непосещённой вершины.
    Каждый запуск «раскрашивает» одну компоненту.

    Сложность: O(V + E) — суммарно каждая вершина и ребро
    обрабатываются ровно один раз.
    """
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            # Запускаем BFS из этой вершины
            component = bfs(graph, vertex)
            visited.update(component)
            components.append(component)

    return components


# ══════════════════════════════════════════════════════════════════
#  ГЛАВНАЯ ПРОГРАММА — запуск всех заданий
# ══════════════════════════════════════════════════════════════════

def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    #  Задание 1.1
    separator("1.1  Матрица смежности")
    matrix = build_adjacency_matrix(edges, vertices)
    print_matrix(matrix, vertices)

    # 1.2
    separator("1.2  Список смежности")
    graph = build_adjacency_list(edges, vertices)
    for v in vertices:
        print(f"  {v} → {graph[v]}")

    #Задание 1.3
    separator("1.3  Степени вершин")
    for v in vertices:
        print(f"  deg({v}) = {degree(graph, v)}")

    # 1.4
    separator("1.4  Проверка теоремы Эйлера")
    check_euler(graph, edges)

    # Задание 2.1
    separator("2.1  Обход BFS из вершины A")
    order = bfs(graph, 'A')
    print(f"  Порядок обхода: {order}")

    # Задание 2.2
    separator("2.2  Расстояния от вершины A")
    dist = bfs_distances(graph, 'A')
    for v in vertices:
        print(f"  A → {v} : {dist[v]} пересадок")

    # Задание 2.3 + 2.4
    separator("2.3–2.4  Кратчайшие пути")

    path_af = bfs_shortest_path(graph, 'A', 'F')
    print(f"  A → F: {path_af}, длина: {len(path_af) - 1}")

    path_df = bfs_shortest_path(graph, 'D', 'F')
    print(f"  D → F: {path_df}, длина: {len(path_df) - 1}")

    # Дополнительное задание
    separator("Доп. задание — Компоненты связности")

    # Расширяем граф: добавляем G (изолированный) и H–I (отдельное ребро)
    extended_edges = edges + [('H', 'I')]
    extended_vertices = vertices + ['G', 'H', 'I']

    ext_graph = build_adjacency_list(extended_edges, extended_vertices)

    print("  Расширенный граф:")
    for v in extended_vertices:
        print(f"    {v} → {ext_graph[v]}")

    components = find_connected_components(ext_graph)
    print(f"\n  Найдено компонент связности: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"    Компонента {i}: {comp}")

    if len(components) > 1:
        print("\n Не все узлы связаны с основным складом!")
        print("  Узлы, требующие отдельной логистики:")
        main_component = set(components[0])
        for comp in components[1:]:
            print(f"    {comp}")

    #Таблица сложности
    separator("Оценка сложности (справка)")
    print("""
  ┌─────────────────────────────────┬─────────┬─────────┬─────────┬─────────────────────────┐
  │ Операция                        │ Лучший  │ Средний │ Худший  │ Обоснование             │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ Построение матрицы смежности    │ O(V²+E) │ O(V²+E) │ O(V²+E) │ V²: нулевая матрица     │
  │                                 │         │         │         │ E:  заполнение рёбер    │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ Построение списка смежности     │ O(V+E)  │ O(V+E)  │ O(V+E)  │ V: пустые списки        │
  │                                 │         │         │         │ E: добавление соседей   │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ degree(graph, vertex)           │ O(1)    │ O(1)    │ O(1)    │ len() списка — O(1)     │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ Проверка теоремы Эйлера         │ O(V)    │ O(V)    │ O(V)    │ Проход по всем вершинам │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ bfs(graph, start)               │ O(V+E)  │ O(V+E)  │ O(V+E)  │ Каждая вершина и ребро  │
  │                                 │         │         │         │ обрабатываются 1 раз    │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ bfs_distances(graph, start)     │ O(V+E)  │ O(V+E)  │ O(V+E)  │ Тот же BFS              │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ bfs_shortest_path(start, end)   │ O(1)    │ O(V+E)  │ O(V+E)  │ Лучший: start == end    │
  │                                 │         │         │         │ Худший: end недостижима  │
  ├─────────────────────────────────┼─────────┼─────────┼─────────┼─────────────────────────┤
  │ find_connected_components       │ O(V+E)  │ O(V+E)  │ O(V+E)  │ Суммарно: один полный   │
  │                                 │         │         │         │ обход всего графа       │
  └─────────────────────────────────┴─────────┴─────────┴─────────┴─────────────────────────┘
""")


if __name__ == "__main__":
    main()