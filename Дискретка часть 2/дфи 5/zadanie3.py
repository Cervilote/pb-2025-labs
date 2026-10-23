# -*- coding: utf-8 -*-
# ЗАДАНИЕ 3. Ввести матрицу смежности [[1,1,1],[1,1,1],[1,0,1]]
# ВВОД:  матрица смежности (ориентированный граф, есть петли)
# ВЫВОД: 1) спектр графа (с обозначением рёбер/дуг)
#        2) рисунок графа (файл risunok_zadanie3.png)
#        3) спектр графа вычислением в тетради -> tetrad.txt
#        4) спектр матрицы программно (та же программа, что в задании 2)
# Запуск: python zadanie3.py      (нужны numpy и matplotlib)
import numpy as np

import os
def risunok_path(imya):
    """Рисунки сохраняются в папку C:\\арбуз (Windows);
    на других системах или при ошибке - рядом со скриптом."""
    papka = r'C:\арбуз' if os.name == 'nt' else '.'
    try:
        os.makedirs(papka, exist_ok=True)
    except OSError:
        papka = '.'
    return os.path.join(papka, imya)

# ==================== ВВОД ====================
A = np.array([          # матрица смежности (то, что мы ВВОДИМ)
    [1, 1, 1],
    [1, 1, 1],
    [1, 0, 1]], dtype=float)
EDG = [(i + 1, j + 1) for i in range(3) for j in range(3) if A[i][j]]  # дуги e1..e8

# ---------------- вспомогательные функции (те же, что в задании 2) ----------------
def poly_str(c):
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

def draw_digraph(M, edges, fname, title):
    """Рисует ориентированный граф по матрице смежности и сохраняет в PNG."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import math
    n = len(M)
    pos = [(math.cos(math.pi / 2 - 2 * math.pi * i / n),
            math.sin(math.pi / 2 - 2 * math.pi * i / n)) for i in range(n)]
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    rn = 0.13
    for k, (u, v) in enumerate(edges, start=1):
        x1, y1 = pos[u - 1]
        x2, y2 = pos[v - 1]
        if u == v:                                   # петля
            ax.add_patch(plt.Circle((x1 * 1.31, y1 * 1.31), 0.18, fill=False, lw=1.5))
            ax.text(x1 * 1.68, y1 * 1.68, f'e{k}', fontsize=10, ha='center')
        else:                                        # дуга со стрелкой
            rad = 0.25 if M[v - 1][u - 1] else 0.0   # изгиб, если есть обратная дуга
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle='-|>', lw=1.5, color='k',
                                        shrinkA=16, shrinkB=18,
                                        connectionstyle=f'arc3,rad={rad}'))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            ln = math.hypot(dx, dy)
            off = rad if rad else 0.09
            ax.text(mx - dy / ln * off, my + dx / ln * off, f'e{k}',
                    fontsize=10, ha='center', va='center')
    for i, (x, y) in enumerate(pos):
        ax.add_patch(plt.Circle((x, y), rn, fc='#ff7f7f', ec='k', zorder=3))
        ax.text(x, y, str(i + 1), ha='center', va='center', zorder=4,
                fontsize=13, fontweight='bold')
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.9, 1.9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)
    fig.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close(fig)

# ==================== печать ВВОДА ====================
print('=' * 62)
print('ВВОД (что вводим):')
print('Матрица смежности A (вершины 1,2,3):')
for r in A:
    print('     |' + '  '.join(f'{v:3.0f}' for v in r) + '|')
print('Обозначения рёбер (дуг): ' + ', '.join(f'e{i+1}=({u},{v})' for i, (u, v) in enumerate(EDG)))

# ==================== ВЫВОД ====================
print('=' * 62)
print('ВЫВОД (что получаем):')

# --- 1) спектр графа ---
print('\n1) Спектр графа. Шаг 1. Уравнение: det(A - λI) = 0')
for i, r in enumerate(A):
    print('     |' + '  '.join((f'{int(v)}-λ' if i == j else f'{int(v):>4}')
                               for j, v in enumerate(r)) + '|')
p = np.poly(A)
print('   Шаг 2. Раскрытое уравнение: ' + poly_str(p) + ' = 0')
print('   Спектр графа = собственные числа матрицы смежности:')
print('   ' + eig_str(A))

# --- 2) рисунок графа ---
FNAME = risunok_path('risunok_zadanie3.png')
draw_digraph(A, EDG, FNAME, 'Задание 3: граф по матрице смежности')
print('\n2) Рисунок графа сохранён в файл:', FNAME)

# --- 3) тетрадь ---
print('\n3) Вычисление спектра в тетради - см. файл tetrad.txt')

# --- 4) спектр матрицы программно (программа из задания 2) ---
print('\n4) Спектр матрицы программно (numpy.linalg.eigvals):')
print('   ' + eig_str(A))
print('   Точно: λ = 0; (3-√5)/2; (3+√5)/2')
print('=' * 62)
