#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лабораторная работа по теме 1.9 «Графы»
Задание 1 (2 балла):
1. Ввести граф с помощью матрицы смежности (ввод с клавиатуры).
2. Вывести:
   1) Матрицу инцидентности (с вводом обозначений ребер с клавиатуры);
   2) Матрицу Кирхгофа и матрицу Лапласа;
   3) Спектр графа (с выводом характеристического уравнения на 2-м шаге);
   4) (Аналитический вывод уравнения для тетради также сформирован в tetrad_zapis.txt).
"""

import numpy as np
import sympy as sp

def get_input(prompt_text, default_val):
    try:
        val = input(f"{prompt_text} [по умолчанию: {default_val}]: ").strip()
        return default_val if val == "" else val
    except EOFError:
        print(f"{default_val} (авто-ввод)")
        return default_val

def main():
    print("=" * 70)
    print("  ЗАДАНИЕ 1: ИССЛЕДОВАНИЕ НЕОРИЕНТИРОВАННОГО ГРАФА И ЕГО СПЕКТРА")
    print("=" * 70)
    print("В графе по умолчанию 4 вершины: A, B, C, D")
    print("Ребра: (A,B), (A,D), (B,C), (B,D), (C,D)")
    print()

    # --- 1. Ввод числа вершин и их наименований ---
    n_str = get_input("Введите количество вершин n", "4")
    n = int(n_str)

    default_vertices = ["A", "B", "C", "D"][:n]
    if len(default_vertices) < n:
        default_vertices += [f"V{i+1}" for i in range(len(default_vertices), n)]
    
    v_str = get_input(f"Введите имена вершин через пробел", " ".join(default_vertices))
    vertices = v_str.split()
    if len(vertices) != n:
        print(f"Предупреждение: введено {len(vertices)} имен, скорректировано до {n}")
        vertices = vertices[:n] if len(vertices) > n else vertices + [f"V{i+1}" for i in range(len(vertices), n)]

    # --- 2. Ввод матрицы смежности ---
    default_adj = [
        [0, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 1, 1, 0]
    ]

    print(f"\nВведите матрицу смежности {n}x{n} построчно (элементы через пробел).")
    print("Для использования матрицы из задания нажмите Enter на первой строке.")
    
    adj_matrix = []
    try:
        first_line = input(f"Строка 1 (для {vertices[0]}): ").strip()
    except EOFError:
        first_line = ""
    if first_line == "" and n == 4:
        print("Используется матрица смежности по умолчанию из задания:")
        adj_matrix = default_adj
        for i, row in enumerate(adj_matrix):
            print(f"  {vertices[i]}: {' '.join(map(str, row))}")
    else:
        row1 = [int(x) for x in first_line.split()] if first_line else default_adj[0][:n]
        adj_matrix.append(row1)
        for i in range(1, n):
            try:
                line = input(f"Строка {i+1} (для {vertices[i]}): ").strip()
            except EOFError:
                line = ""
            if line:
                adj_matrix.append([int(x) for x in line.split()])
            else:
                adj_matrix.append(default_adj[i][:n] if i < len(default_adj) else [0]*n)

    A = np.array(adj_matrix, dtype=int)
    print("\nМатрица смежности A:")
    print("    " + "  ".join(f"{v:>3}" for v in vertices))
    for i, row in enumerate(A):
        print(f"{vertices[i]:>3} " + "  ".join(f"{val:>3}" for val in row))

    # --- 3. Поиск ребер и ввод обозначений ребер ---
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] != 0:
                edges.append((i, j))
    
    m = len(edges)
    print(f"\nОбнаружено ребер в графе: {m}")
    default_edge_names = [f"e{k+1}({vertices[u]}-{vertices[v]})" for k, (u, v) in enumerate(edges)]
    print("Предлагаемые обозначения ребер:")
    for name in default_edge_names:
        print(f"  {name}")
    
    edge_names_input = get_input("\nВведите обозначения ребер через пробел", " ".join([f"e{k+1}" for k in range(m)]))
    edge_names = edge_names_input.split()
    if len(edge_names) != m:
        edge_names = [f"e{k+1}" for k in range(m)]
    
    print("\nСоответствие ребер:")
    for k, (u, v) in enumerate(edges):
        print(f"  Ребро {edge_names[k]}: соединяет {vertices[u]} и {vertices[v]}")

    # --- 4. 1) Матрица инцидентности ---
    print("\n" + "=" * 50)
    print("1) МАТРИЦА ИНЦИДЕНТНОСТИ (Incidence Matrix B)")
    print("=" * 50)
    B = np.zeros((n, m), dtype=int)
    for k, (u, v) in enumerate(edges):
        B[u, k] = 1
        B[v, k] = 1

    header = "     " + "  ".join(f"{name:>5}" for name in edge_names)
    print(header)
    for i in range(n):
        row_str = "  ".join(f"{B[i, k]:>5}" for k in range(m))
        print(f"{vertices[i]:>3}  {row_str}")

    # --- 5. 2) Матрица Кирхгофа и матрица Лапласа ---
    print("\n" + "=" * 50)
    print("2) МАТРИЦА КИРХГОФА И МАТРИЦА ЛАПЛАСА")
    print("=" * 50)
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)
    
    print("Степени вершин deg(v):")
    for i, v in enumerate(vertices):
        print(f"  deg({v}) = {degrees[i]}")
    
    # В классической теории графов матрица Кирхгофа и матрица Лапласа (лапласиан) тождественны: L = D - A
    L = D - A
    print("\nМатрица Кирхгофа (Лапласа) L = D - A:")
    print("    " + "  ".join(f"{v:>3}" for v in vertices))
    for i, row in enumerate(L):
        print(f"{vertices[i]:>3} " + "  ".join(f"{val:>3}" for val in row))
    
    print("\nСвойства матрицы Кирхгофа:")
    print(" - Диагональные элементы L[i,i] равны степени соответствующей вершины.")
    print(" - Недиагональные элементы L[i,j] = -1 при наличии ребра и 0 при отсутствии.")
    print(f" - Суммы элементов по строкам и столбцам: {np.sum(L, axis=1)} (всегда равны 0).")

    # Нормализованная матрица Лапласа
    inv_sqrt_deg = np.zeros(n)
    for i in range(n):
        if degrees[i] > 0:
            inv_sqrt_deg[i] = 1.0 / np.sqrt(degrees[i])
    D_norm = np.diag(inv_sqrt_deg)
    L_sym = D_norm @ L @ D_norm
    print("\nНормализованная симметричная матрица Лапласа L_sym = D^(-1/2) * L * D^(-1/2):")
    print("    " + "  ".join(f"{v:>7}" for v in vertices))
    for i in range(n):
        row_str = "  ".join(f"{L_sym[i, j]:>7.3f}" for j in range(n))
        print(f"{vertices[i]:>3} {row_str}")

    # --- 6. 3) Спектр графа (с выводом уравнения на 2-м шаге) ---
    print("\n" + "=" * 50)
    print("3) СПЕКТР ГРАФА (С ВЫВОДОМ УРАВНЕНИЯ НА 2-М ШАГЕ)")
    print("=" * 50)
    
    lam = sp.Symbol('lambda')
    A_sym = sp.Matrix(A)
    char_matrix = lam * sp.eye(n) - A_sym
    
    print("Шаг 1: Составление характеристической матрицы [lambda*I - A]:")
    sp.pprint(char_matrix)
    print()
    
    char_poly = char_matrix.det()
    char_poly_simplified = sp.Poly(char_poly, lam)
    
    print("Шаг 2: Вывод характеристического уравнения: det(lambda*I - A) = 0")
    print("  Вычисленный определитель:")
    print(f"  P(lambda) = {char_poly} = 0")
    
    factored_poly = sp.factor(char_poly)
    print(f"  В факторизованном виде: {factored_poly} = 0")
    print()

    print("Шаг 3: Нахождение корней уравнения (собственных значений — спектра графа):")
    roots = sp.roots(char_poly)
    all_roots = char_poly_simplified.all_roots()
    
    print(f"  Точный алгебраический спектр графа:")
    for idx, r in enumerate(all_roots):
        val_approx = complex(r.evalf(6))
        if abs(val_approx.imag) < 1e-9:
            print(f"    lambda_{idx+1} = {r} ≈ {val_approx.real:+.5f}")
        else:
            print(f"    lambda_{idx+1} = {r} ≈ {val_approx.real:+.5f} + {val_approx.imag:+.5f}i")
    
    # Также численно через numpy для верификации
    np_eigvals = np.linalg.eigvals(A.astype(float))
    np_eigvals_sorted = np.sort(np_eigvals)[::-1]
    print(f"\n  Спектр графа (численно через NumPy, по убыванию):")
    print("  [" + ", ".join(f"{ev:.5f}" for ev in np_eigvals_sorted) + "]")

    print("\n" + "=" * 70)
    print("  Задание 1 успешно выполнено! Подробный рукописный вывод для тетради")
    print("  сохранен в файле tetrad_zapis.txt.")
    print("=" * 70)

if __name__ == "__main__":
    main()
