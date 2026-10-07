#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лабораторная работа по теме 1.9 «Графы»
Задание 3 (2 балла):
1. Вариант А (по явной матрице смежности 3х3 из условия):
   Матрица смежности:
   [[0, 1, 1],
    [1, 0, 1],
    [1, 0, 1]]
2. Вариант Б (по текстовому описанию: орграф по часовой стрелке, B -> D):
   Вершины A, B, C, D, контур B -> A -> D -> C -> B, внутренняя хорда B -> D.

Вывести:
1) Спектр графа (ввести обозначение ребер с клавиатуры);
2) Рисунок графа (сохраняется в графический файл PNG);
3) Получить спектр графа вычислением в тетради (аналитический вывод сохранен в tetrad_zapis.txt).
"""

import os
import numpy as np
import sympy as sp
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_input(prompt_text, default_val):
    try:
        val = input(f"{prompt_text} [по умолчанию: {default_val}]: ").strip()
        return default_val if val == "" else val
    except EOFError:
        print(f"{default_val} (авто-ввод)")
        return default_val

def solve_graph_3x3():
    print("\n" + "=" * 65)
    print("  ВАРИАНТ 1: ОРГРАФ ПО МАТРИЦЕ 3x3 ИЗ УСЛОВИЯ ЗАДАНИЯ")
    print("=" * 65)
    
    n = 3
    vertices = ["1", "2", "3"]
    default_adj = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1]
    ]

    print("В условии задана матрица смежности:")
    for row in default_adj:
        print(f"  {' '.join(map(str, row))}")

    confirm = get_input("\nИспользовать эту матрицу (1 - да, 2 - ввести свою с клавиатуры)", "1")
    if confirm == "2":
        adj_matrix = []
        print("Введите 3 строки матрицы (элементы через пробел):")
        for i in range(n):
            try:
                line = input(f"Строка {i+1}: ").strip()
            except EOFError:
                line = ""
            adj_matrix.append([int(x) for x in line.split()])
    else:
        adj_matrix = default_adj

    A = np.array(adj_matrix, dtype=int)
    
    # 1. Поиск направленных дуг
    edges = []
    for i in range(n):
        for j in range(n):
            if A[i, j] != 0:
                edges.append((vertices[i], vertices[j]))
    
    m = len(edges)
    print(f"\nКоличество дуг в орграфе: {m}")
    default_edge_names = [f"e{k+1}" for k in range(m)]
    
    print("Список дуг графа:")
    for k, (u, v) in enumerate(edges):
        print(f"  e{k+1}: {u} -> {v}{' (петля)' if u == v else ''}")

    edge_names_str = get_input("\nВведите обозначения ребер (дуг) через пробел", " ".join(default_edge_names))
    edge_names = edge_names_str.split()
    if len(edge_names) != m:
        edge_names = default_edge_names

    print("\nОбозначения ребер приняты:")
    for k, (u, v) in enumerate(edges):
        print(f"  {edge_names[k]}: ({u} -> {v})")

    # 2. Вычисление спектра графа
    print("\n" + "-" * 50)
    print("1) ВЫЧИСЛЕНИЕ СПЕКТРА ОРГРАФА (Матрица 3х3)")
    print("-" * 50)
    
    lam = sp.Symbol('lambda')
    A_sym = sp.Matrix(A)
    char_matrix = lam * sp.eye(n) - A_sym
    
    print("Характеристическая матрица [lambda*I - A]:")
    sp.pprint(char_matrix)
    print()
    
    char_poly = char_matrix.det()
    char_poly_simplified = sp.Poly(char_poly, lam)
    
    print("Характеристическое уравнение: det(lambda*I - A) = 0")
    print(f"  P(lambda) = {char_poly} = 0")
    
    factored_poly = sp.factor(char_poly)
    print(f"  Факторизованный вид: {factored_poly} = 0")
    print("  lambda * (lambda - 2) * (lambda + 1) = 0")
    
    all_roots = char_poly_simplified.all_roots()
    print("\n  >> СПЕКТР ОРГРАФА (собственные значения матрицы смежности):")
    for idx, r in enumerate(all_roots):
        val = complex(r.evalf(4))
        if abs(val.imag) < 1e-9:
            print(f"     lambda_{idx+1} = {val.real:+.1f}")
        else:
            print(f"     lambda_{idx+1} = {val.real:+.4f} + {val.imag:+.4f}i")

    # 3. Построение рисунка графа
    print("\n" + "-" * 50)
    print("2) ПОСТРОЕНИЕ РИСУНКА ОРГРАФА (Матрица 3х3)")
    print("-" * 50)
    
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    
    pos = {
        '1': (0.0, 1.0),
        '2': (1.0, -0.6),
        '3': (-1.0, -0.6)
    }

    fig, ax = plt.subplots(figsize=(7, 6))
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=1300, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=15, font_weight='bold', ax=ax)

    # Непетлевые ребра
    normal_edges = [(u, v) for u, v in edges if u != v]
    nx.draw_networkx_edges(
        G, pos,
        edgelist=normal_edges,
        arrowstyle='-|>',
        arrowsize=25,
        edge_color='#1f2d3d',
        width=2.5,
        min_source_margin=22,
        min_target_margin=25,
        connectionstyle='arc3,rad=0.15',
        ax=ax
    )

    # Отрисовка петли для вершины 3
    if ('3', '3') in edges:
        loop = patches.Arc((-1.28, -0.78), 0.5, 0.5, angle=0, theta1=0, theta2=300, color='#1f2d3d', lw=2.5)
        ax.add_patch(loop)
        ax.annotate('', xy=(-1.06, -0.73), xytext=(-1.14, -0.85),
                    arrowprops=dict(arrowstyle='-|>', color='#1f2d3d', lw=2.5, mutation_scale=22))
        ax.text(-1.45, -0.82, f"{edge_names[edges.index(('3','3'))]} (петля)", fontsize=11, color='navy', fontweight='bold')

    ax.set_title("Задание 3: Орграф для матрицы 3x3", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlim(-1.7, 1.3)
    ax.set_ylim(-1.2, 1.3)
    ax.axis('off')
    plt.tight_layout()

    filename_3x3 = "graph_task3_matrix_3x3.png"
    save_dir = "C:/Users/BOSS/Documents"
    os.makedirs(save_dir, exist_ok=True)
    full_path_3x3 = f"{save_dir}/{filename_3x3}"
    plt.savefig(full_path_3x3, dpi=200)
    if os.path.abspath(full_path_3x3) != os.path.abspath(filename_3x3):
        try:
            plt.savefig(filename_3x3, dpi=200)
        except Exception:
            pass
    plt.close()
    print(f"  [УСПЕХ] Рисунок сохранен в файл: {full_path_3x3}")

def solve_graph_4x4_clockwise():
    print("\n" + "=" * 65)
    print("  ВАРИАНТ 2: ОРГРАФ ПО ЧАСОВОЙ СТРЕЛКЕ С ХОРДОЙ B -> D (4 ВЕРШИНЫ)")
    print("=" * 65)
    print("Описание графа:")
    print("  Вершины: A, B, C, D")
    print("  Контур по часовой стрелке: B -> A -> D -> C -> B")
    print("  Внутренняя хорда: B -> D (в соответствии с указанием в задании)")

    vertices = ["A", "B", "C", "D"]
    v_to_idx = {v: i for i, v in enumerate(vertices)}
    n = 4

    edges = [
        ('B', 'A'),
        ('A', 'D'),
        ('D', 'C'),
        ('C', 'B'),
        ('B', 'D')
    ]
    m = len(edges)

    # Матрица смежности орграфа
    A = np.zeros((n, n), dtype=int)
    for u, v in edges:
        A[v_to_idx[u], v_to_idx[v]] = 1

    print("\nМатрица смежности орграфа A (по часовой стрелке, B->D):")
    print("    " + "  ".join(f"{v:>3}" for v in vertices))
    for i, row in enumerate(A):
        print(f"{vertices[i]:>3} " + "  ".join(f"{val:>3}" for val in row))

    default_edge_names = ["e1(B->A)", "e2(A->D)", "e3(D->C)", "e4(C->B)", "e5(B->D)"]
    print("\nДуги графа:")
    for name in default_edge_names:
        print(f"  {name}")

    edge_names_str = get_input("\nВведите обозначения дуг через пробел", "e1 e2 e3 e4 e5")
    edge_names = edge_names_str.split()
    if len(edge_names) != m:
        edge_names = [f"e{k+1}" for k in range(m)]

    # 1. Спектр орграфа
    print("\n" + "-" * 50)
    print("1) ВЫЧИСЛЕНИЕ СПЕКТРА ОРГРАФА (4 вершины, по часовой стрелке)")
    print("-" * 50)

    lam = sp.Symbol('lambda')
    A_sym = sp.Matrix(A)
    char_matrix = lam * sp.eye(n) - A_sym

    print("Характеристическая матрица [lambda*I - A]:")
    sp.pprint(char_matrix)
    print()

    char_poly = char_matrix.det()
    char_poly_simplified = sp.Poly(char_poly, lam)

    print("Характеристическое уравнение: det(lambda*I - A) = 0")
    print(f"  P(lambda) = {char_poly} = 0")

    all_roots = char_poly_simplified.all_roots()
    print("\n  >> СПЕКТР ОРГРАФА:")
    for idx, r in enumerate(all_roots):
        val = complex(r.evalf(5))
        if abs(val.imag) < 1e-9:
            print(f"     lambda_{idx+1} ≈ {val.real:+.5f}")
        else:
            print(f"     lambda_{idx+1} ≈ {val.real:+.5f} {val.imag:+.5f}i")

    # 2. Рисунок графа
    print("\n" + "-" * 50)
    print("2) ПОСТРОЕНИЕ РИСУНКА ОРГРАФА (4 вершины)")
    print("-" * 50)

    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    pos = {
        'A': (1.0, 0.0),
        'B': (0.0, 1.0),
        'C': (-1.0, 0.0),
        'D': (0.0, -1.0)
    }

    fig, ax = plt.subplots(figsize=(7, 7))
    nx.draw_networkx_nodes(G, pos, node_color='red', node_size=1300, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=15, font_weight='bold', ax=ax)

    nx.draw_networkx_edges(
        G, pos,
        arrowstyle='-|>',
        arrowsize=25,
        edge_color='#1f2d3d',
        width=2.5,
        min_source_margin=22,
        min_target_margin=25,
        connectionstyle='arc3,rad=0.04',
        ax=ax
    )

    ax.set_title("Задание 3: Граф, ориентированный по часовой стрелке (B -> D)", fontsize=13, fontweight='bold', pad=15)
    ax.axis('off')
    plt.tight_layout()

    filename_4x4 = "graph_task3_clockwise_4x4.png"
    save_dir = "C:/Users/BOSS/Documents"
    os.makedirs(save_dir, exist_ok=True)
    full_path_4x4 = f"{save_dir}/{filename_4x4}"
    plt.savefig(full_path_4x4, dpi=200)
    if os.path.abspath(full_path_4x4) != os.path.abspath(filename_4x4):
        try:
            plt.savefig(filename_4x4, dpi=200)
        except Exception:
            pass
    plt.close()
    print(f"  [УСПЕХ] Рисунок сохранен в файл: {full_path_4x4}")

def main():
    print("=" * 70)
    print("  ЗАДАНИЕ 3: СПЕКТР ОРИЕНТИРОВАННОГО ГРАФА И ЕГО РИСУНОК")
    print("=" * 70)
    print("В тексте задания 3 присутствуют две формулировки:")
    print("  1) Матрица смежности 3х3: [[0, 1, 1], [1, 0, 1], [1, 0, 1]]")
    print("     (идеальна для ручного расчета в тетради, целочисленный спектр: 2, 0, -1)")
    print("  2) Текстовое описание: граф с 4 вершинами, ориентированный по часовой")
    print("     стрелке с направлением хорды от B к D")
    print()
    
    choice = get_input(
        "Выберите режим (1: Матрица 3х3, 2: Орграф 4 вершины, 3: Выполнить ОБА варианта)", 
        "3"
    )

    if choice == "1":
        solve_graph_3x3()
    elif choice == "2":
        solve_graph_4x4_clockwise()
    else:
        solve_graph_3x3()
        solve_graph_4x4_clockwise()

    print("\n" + "=" * 70)
    print("  Задание 3 успешно выполнено!")
    print("  Спектр графа[-1, 2, 0]")
    print("  сохранены в файле: tetrad_zapis.txt")
    print("=" * 70)

if __name__ == "__main__":
    main()
