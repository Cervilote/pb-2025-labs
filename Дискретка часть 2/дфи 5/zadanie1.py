# -*- coding: utf-8 -*-
# ЗАДАНИЕ 1. Граф из методички: вершины A, B, C, D
# рёбра: A-B, A-D, B-C, B-D, C-D  (e1..e5)
# ВВОД:  матрица смежности
# ВЫВОД: 1) матрица инцидентности (с обозначением рёбер)
#        2) матрица Кирхгофа и матрица Лапласа
#        3) спектр графа (уравнение выводится на 2-м шаге)
#        4) уравнение для тетради -> см. файл tetrad.txt
# Запуск: python zadanie1.py      (нужен только numpy)
import numpy as np

# ==================== ВВОД ====================
VER = ['A', 'B', 'C', 'D']                                    # имена вершин
EDG = [('A', 'B'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]  # рёбра e1..e5
A = np.array([          # матрица смежности (то, что мы ВВОДИМ)
    [0, 1, 0, 1],
    [1, 0, 1, 1],
    [0, 1, 0, 1],
    [1, 1, 1, 0]], dtype=float)

# ---------------- вспомогательные функции ----------------
def show(M, rows=None, cols=None):
    """Красиво печатает матрицу."""
    if cols:
        print('      ' + '  '.join(f'{c:>5}' for c in cols))
    for i, r in enumerate(M):
        name = rows[i] if rows else str(i + 1)
        print(f'  {name:>2} |' + '  '.join(f'{v:5.0f}' for v in r))

def poly_str(c):
    """Строка вида 'λ^4 - 5λ^2 - 4λ' из коэффициентов (от старшей степени)."""
    n = len(c) - 1
    c = [round(x, 6) for x in c]
    c = [int(x) if abs(x - round(x)) < 1e-6 else x for x in c]
    out = []
    for k, a in enumerate(c):
        p = n - k
        if a == 0:
            continue
        s = '-' if a < 0 else ('+' if out else '')
        v = abs(a)
        lam = '' if p == 0 else ('λ' if p == 1 else f'λ^{p}')
        coef = '' if (lam and v == 1) else str(v)
        out.append(f'{s} {coef}{lam}'.strip())
    return ' '.join(out) if out else '0'

def eig_str(M):
    """Собственные числа матрицы M одной строкой (по убыванию Re)."""
    w = sorted(np.linalg.eigvals(M), key=lambda z: -z.real)
    res = []
    for z in w:
        re_, im_ = z.real, z.imag
        if abs(re_) < 1e-9: re_ = 0.0
        if abs(im_) < 1e-9: im_ = 0.0
        if im_ == 0.0:
            res.append(f'{re_:.4f}')
        else:
            res.append(f'{re_:.4f}{im_:+.4f}i')
    return '{ ' + '; '.join(res) + ' }'

# ==================== печать ВВОДА ====================
print('=' * 62)
print('ВВОД (что вводим):')
print('Матрица смежности A (строки/столбцы - вершины A,B,C,D):')
show(A, VER, VER)
print('Обозначения рёбер: ' + ', '.join(f'e{i+1}={u}{v}' for i, (u, v) in enumerate(EDG)))

# ==================== ВЫВОД ====================
print('=' * 62)
print('ВЫВОД (что получаем):')

# --- 1) матрица инцидентности ---
n, m = len(VER), len(EDG)
B = np.zeros((n, m))
for k, (u, v) in enumerate(EDG):
    B[VER.index(u)][k] = 1
    B[VER.index(v)][k] = 1
print('\n1) Матрица инцидентности (строки - вершины, столбцы - рёбра e1..e5):')
show(B, VER, [f'e{i+1}' for i in range(m)])

# --- 2) Кирхгоф и Лаплас ---
Bs = np.zeros((n, m))            # знаковая инцидентность (-1 начало, +1 конец)
for k, (u, v) in enumerate(EDG):
    Bs[VER.index(u)][k] = -1
    Bs[VER.index(v)][k] = 1
K = Bs @ Bs.T                    # матрица Кирхгофа = B * B^T
D = np.diag(A.sum(axis=1))       # степени вершин
L = D - A                        # матрица Лапласа = D - A
print('\n2) Матрица Кирхгофа (B*B^T):')
show(K, VER, VER)
print('   Матрица Лапласа (D - A):')
show(L, VER, VER)
print('   Матрицы совпадают:', np.allclose(K, L))

# --- 3) спектр графа с уравнением ---
print('\n3) Шаг 1. Уравнение в виде определителя: det(A - λI) = 0')
for i, r in enumerate(A):
    print('     |' + '  '.join((f'{int(v)}-λ' if i == j else f'{int(v):>4}')
                               for j, v in enumerate(r)) + '|')
p = np.poly(A)                   # характеристический многочлен det(λI - A)
print('   Шаг 2. Раскрытое уравнение: ' + poly_str(p) + ' = 0')
print('   Спектр графа (собственные числа A):        ' + eig_str(A))
print('   Спектр Лапласа (собственные числа L):      ' + eig_str(L))

# --- 4) уравнение для тетради ---
print('\n4) Уравнение для тетради: ' + poly_str(p) + ' = 0   (записано в tetrad.txt)')
print('=' * 62)
