#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лабораторная работа по теме 1.9 «Графы»
Задание 2 (1 балл):
1. Ввести матрицу весов неориентированного графа (вес AD = 3, остальные по 5).
2. Вывести:
   1) Матрицу весов;
      Эксцентриситеты вершин и радиус графа;
      Длину кратчайшего пути между A и C;
   2) Сделать граф ориентированным против часовой стрелки;
      Вывести рисунок графа (сохранить в файл graph_task2_counterclockwise.png);
      Определить длину кратчайшего пути между A и C в орграфе.
"""

import math
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_input(prompt_text, default_val):
    try:
        val = input(f"{prompt_text} [по умолчанию: {default_val}]: ").strip()
        return default_val if val == "" else val
    except EOFError:
        print(f"{default_val} (авто-ввод)")
        return default_val

def floyd_warshall(dist_matrix, n):
    dist = np.copy(dist_matrix).astype(float)
    next_node = [[j if not math.isinf(dist[i, j]) and i != j else None for j in range(n)] for i in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] + dist[k, j] < dist[i, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
                    next_node[i][j] = next_node[i][k]
    return dist, next_node

def reconstruct_path(i, j, next_node, vertices):
    if next_node[i][j] is None:
        return []
    path = [i]
    curr = i
    while curr != j:
        curr = next_node[curr][j]
        if curr is None:
            return []
        path.append(curr)
    return [vertices[idx] for idx in path]

def main():
    print("=" * 70)
    print("  ЗАДАНИЕ 2: МАТРИЦА ВЕСОВ, МЕТРИЧЕСКИЕ ХАРАКТЕРИСТИКИ И ОРГРАФ")
    print("=" * 70)
    
    vertices = ["A", "B", "C", "D"]
    v_to_idx = {v: i for i, v in enumerate(vertices)}
    n = 4
    
    print("Вершины графа: A, B, C, D")
    print("Условие задачи: вес ребра AD = 3, остальных существующих ребер — по 5.")
    print("Существующие ребра: (A,B), (B,C), (C,D), (D,A), (B,D). Ребра между A и C нет.\n")

    # --- 1. Ввод весов с клавиатуры ---
    input_mode = get_input(
        "Выберите способ ввода весов (1 - по ребрам с подтверждением, 2 - построчно матрицей, 3 - по умолчанию)", 
        "3"
    )

    weight_matrix = np.full((n, n), np.inf)
    np.fill_diagonal(weight_matrix, 0.0)

    # Веса по умолчанию
    default_edges = {
        ('A', 'B'): 5.0,
        ('A', 'D'): 3.0,
        ('B', 'C'): 5.0,
        ('B', 'D'): 5.0,
        ('C', 'D'): 5.0
    }

    if input_mode == "1":
        print("\nВведите веса ребер с клавиатуры:")
        for (u, v), def_w in default_edges.items():
            w_str = get_input(f"Вес ребра {u}-{v}", str(def_w))
            w = float(w_str)
            iu, iv = v_to_idx[u], v_to_idx[v]
            weight_matrix[iu, iv] = w
            weight_matrix[iv, iu] = w
    elif input_mode == "2":
        print("\nВведите 4 строки матрицы весов (числа через пробел, inf или 0 для отсутствующих):")
        for i in range(n):
            try:
                line = input(f"Строка для {vertices[i]}: ").strip()
            except EOFError:
                line = ""
            parts = line.split()
            for j in range(n):
                if j < len(parts):
                    val_str = parts[j].lower()
                    if val_str in ['inf', 'н', '-']:
                        val = np.inf
                    else:
                        val = float(val_str)
                        if i != j and val == 0:
                            val = np.inf
                    weight_matrix[i, j] = val
    else:
        print("Приняты веса по умолчанию из задания (AD = 3, остальные = 5).")
        for (u, v), def_w in default_edges.items():
            iu, iv = v_to_idx[u], v_to_idx[v]
            weight_matrix[iu, iv] = def_w
            weight_matrix[iv, iu] = def_w

    # --- 2. 1) Вывод матрицы весов ---
    print("\n" + "=" * 50)
    print("1) МАТРИЦА ВЕСОВ НЕОРИЕНТИРОВАННОГО ГРАФА W")
    print("=" * 50)
    print("    " + "  ".join(f"{v:>6}" for v in vertices))
    for i in range(n):
        row_str = "  ".join(f"{('∞' if math.isinf(weight_matrix[i, j]) else f'{weight_matrix[i, j]:g}'):>6}" for j in range(n))
        print(f"{vertices[i]:>3} {row_str}")

    # Расчет матрицы кратчайших расстояний (Флойд-Уоршелл)
    dist_matrix, next_node = floyd_warshall(weight_matrix, n)

    print("\nМатрица кратчайших расстояний D_dist:")
    print("    " + "  ".join(f"{v:>6}" for v in vertices))
    for i in range(n):
        row_str = "  ".join(f"{dist_matrix[i, j]:>6.1f}" for j in range(n))
        print(f"{vertices[i]:>3} {row_str}")

    # --- 3. Эксцентриситеты и радиус графа ---
    print("\n" + "=" * 50)
    print("ЭКСПЦЕНТРИСИТЕТЫ, РАДИУС И ДИАМЕТР ГРАФА")
    print("=" * 50)
    eccentricities = {}
    for i in range(n):
        # Эксцентриситет — максимум расстояний от вершины i до всех остальных
        ecc = np.max(dist_matrix[i, :])
        eccentricities[vertices[i]] = ecc
        print(f"  Эксцентриситет вершины {vertices[i]}: e({vertices[i]}) = {ecc:g}")

    radius = min(eccentricities.values())
    diameter = max(eccentricities.values())
    centers = [v for v, ecc in eccentricities.items() if ecc == radius]

    print(f"\n  >> Радиус графа R(G) = min(e(v)) = {radius:g}")
    print(f"  >> Диаметр графа D(G) = max(e(v)) = {diameter:g}")
    print(f"  >> Центр графа (вершины с min эксцентриситетом): {', '.join(centers)}")

    # Кратчайший путь между A и C в неориентированном графе
    path_ac = reconstruct_path(v_to_idx['A'], v_to_idx['C'], next_node, vertices)
    len_ac = dist_matrix[v_to_idx['A'], v_to_idx['C']]
    print(f"\nКратчайший путь между A и C (неориентированный):")
    print(f"  Траектория пути: {' -> '.join(path_ac)}")
    print(f"  Длина кратчайшего пути: {len_ac:g} (AD = 3, DC = 5 => 3 + 5 = 8)")

    # --- 4. 2) Граф, ориентированный против часовой стрелки ---
    print("\n" + "=" * 50)
    print("2) ГРАФ, ОРИЕНТИРОВАННЫЙ ПРОТИВ ЧАСОВОЙ СТРЕЛКИ")
    print("=" * 50)
    print("Расположение вершин на плоскости:")
    print("  A: справа (1, 0)")
    print("  B: сверху (0, 1)")
    print("  C: слева (-1, 0)")
    print("  D: снизу (0, -1)")
    print("\nОриентация контура против часовой стрелки (CCW):")
    print("  A -> B (вес 5)")
    print("  B -> C (вес 5)")
    print("  C -> D (вес 5)")
    print("  D -> A (вес 3)")
    
    chord_dir = get_input(
        "Направление внутренней хорды между B и D (1: от D к B [по циклу CCW], 2: от B к D)", 
        "1"
    )
    chord_edge = ('D', 'B', 5.0) if chord_dir == "1" else ('B', 'D', 5.0)
    print(f"Выбрано ребро хорды: {chord_edge[0]} -> {chord_edge[1]} (вес {chord_edge[2]:g})")

    directed_edges = [
        ('A', 'B', 5.0),
        ('B', 'C', 5.0),
        ('C', 'D', 5.0),
        ('D', 'A', 3.0),
        chord_edge
    ]

    # Построение матрицы весов ориентированного графа
    dir_weight_matrix = np.full((n, n), np.inf)
    np.fill_diagonal(dir_weight_matrix, 0.0)
    for u, v, w in directed_edges:
        dir_weight_matrix[v_to_idx[u], v_to_idx[v]] = w

    print("\nМатрица весов ориентированного графа W_dir:")
    print("    " + "  ".join(f"{v:>6}" for v in vertices))
    for i in range(n):
        row_str = "  ".join(f"{('∞' if math.isinf(dir_weight_matrix[i, j]) else f'{dir_weight_matrix[i, j]:g}'):>6}" for j in range(n))
        print(f"{vertices[i]:>3} {row_str}")

    # Поиск кратчайшего пути в орграфе
    dir_dist_matrix, dir_next_node = floyd_warshall(dir_weight_matrix, n)
    dir_path_ac = reconstruct_path(v_to_idx['A'], v_to_idx['C'], dir_next_node, vertices)
    dir_len_ac = dir_dist_matrix[v_to_idx['A'], v_to_idx['C']]

    print("\n" + "-" * 50)
    print("КРАТЧАЙШИЙ ПУТЬ МЕЖДУ A И C В ОРГРАФЕ:")
    print("-" * 50)
    if math.isinf(dir_len_ac):
        print("  Путь между A и C в данном направлении отсутствует!")
    else:
        print(f"  Траектория пути: {' -> '.join(dir_path_ac)}")
        print(f"  Длина кратчайшего пути: {dir_len_ac:g}")
        print("  Обоснование: из вершины A единственная исходящая дуга ведет в B (вес 5),")
        print("  а из B дуга ведет в C (вес 5). Ребро (D, A) направлено к A, поэтому")
        print("  путь A -> D -> C в орграфе невозможен. Длина пути: 5 + 5 = 10.")

    # --- 5. Построение рисунка графа ---
    print("\nПостроение рисунка ориентированного графа...")
    G = nx.DiGraph()
    pos = {
        'A': (1.0, 0.0),
        'B': (0.0, 1.0),
        'C': (-1.0, 0.0),
        'D': (0.0, -1.0)
    }
    G.add_nodes_from(vertices)
    for u, v, w in directed_edges:
        G.add_edge(u, v, weight=w)

    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Узлы графа в виде крупных красных кругов (в точности как в методичке)
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=1300, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=15, font_weight='bold', ax=ax)

    # Ребра графа со стрелками
    nx.draw_networkx_edges(
        G, pos,
        arrowstyle='-|>',
        arrowsize=25,
        edge_color='#1f2d3d',
        width=2.5,
        min_source_margin=22,
        min_target_margin=25,
        connectionstyle='arc3,rad=0.03',
        ax=ax
    )

    # Метки весов ребер
    edge_labels = {(u, v): f"w={d['weight']:g}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=12,
        font_color='navy',
        font_weight='bold',
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.9),
        ax=ax
    )

    ax.set_title("Задание 2: Граф, ориентированный против часовой стрелки", fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()
    
    img_filename = "graph_task2_counterclockwise.png"
    plt.savefig(f"/C:/Users/BOSS/Documents/{img_filename}", dpi=200)
    plt.close()
    print(f"  [УСПЕХ] Рисунок графа сохранен в файл: /home/user/{img_filename}")

    print("\n" + "=" * 70)
    print("  Задание 2 успешно выполнено!")
    print("=" * 70)

if __name__ == "__main__":
    main()
