"""
Лабораторная работа №6 по теме 1.9 «Графы»
Задание 1:
- Ввод неориентированного графа с консоли с помощью матрицы смежности
  (для графа из методички с вершинами A, B, C, D матрица 4x4:
   0 1 0 1
   1 0 1 1
   0 1 0 1
   1 1 1 0)
- Программный вывод:
  1) уравнения для расчёта собственных значений по матрице Кирхгофа
  2) собственных значений и вектора Фидлера (+ разбиение на кластеры и рисунок графа)
"""

import re
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def charpoly_coeffs(M: np.ndarray) -> list[float]:
    """Коэффициенты характеристического многочлена det(λE - M) = 0 (метод Фаддеева — Леверье)."""
    M = np.asarray(M, dtype=float)
    n = M.shape[0]
    coeffs = [1.0]
    B = np.zeros_like(M)
    for k in range(1, n + 1):
        B = M @ (B + coeffs[-1] * np.eye(n)) if k > 1 else M.copy()
        coeffs.append(-np.trace(B) / k)
    return [int(round(c)) if abs(c - round(c)) < 1e-7 else round(c, 6) for c in coeffs]


def format_polynomial(coeffs: list[float], var: str = "λ", negate_odd_det: bool = False) -> str:
    """Форматирует многочлен вида c_0*λ^n + c_1*λ^(n-1) + ... + c_n = 0."""
    deg = len(coeffs) - 1
    if negate_odd_det and deg % 2 == 1:
        coeffs = [-c for c in coeffs]
    terms = []
    for i, c in enumerate(coeffs):
        power = deg - i
        if abs(c) < 1e-9:
            continue
        sign = "-" if c < 0 else "+"
        ac = abs(c)
        coef_str = "" if (ac == 1 and power > 0) else f"{ac}"
        if power == 0:
            monom = f"{ac}"
        elif power == 1:
            monom = f"{coef_str}{var}"
        else:
            monom = f"{coef_str}{var}^{power}"
        if not terms:
            terms.append(f"-{monom}" if c < 0 else monom)
        else:
            terms.append(f"{sign} {monom}")
    return (" ".join(terms) if terms else "0") + " = 0"


def format_det_matrix(L: np.ndarray, var: str = "λ") -> str:
    """Возвращает строковое представление определителя det(L - λE) = 0."""
    n = L.shape[0]
    str_grid = []
    width = 1
    for i in range(n):
        row = []
        for j in range(n):
            val = int(round(L[i, j])) if abs(L[i, j] - round(L[i, j])) < 1e-9 else round(L[i, j], 3)
            cell = f"{val} - {var}" if i == j else f"{val}"
            width = max(width, len(cell))
            row.append(cell)
        str_grid.append(row)
    lines = []
    for idx, row in enumerate(str_grid):
        suffix = " = 0" if idx == n // 2 else ""
        lines.append("  | " + "  ".join(cell.rjust(width) for cell in row) + " |" + suffix)
    return "\n".join(lines)


DEFAULT_A1 = np.array([
    [0, 1, 0, 1],
    [1, 0, 1, 1],
    [0, 1, 0, 1],
    [1, 1, 1, 0],
], dtype=int)
DEFAULT_LABELS1 = ["A", "B", "C", "D"]


def read_adjacency_matrix_from_console(
    default_matrix: np.ndarray = DEFAULT_A1,
    default_labels: list[str] = DEFAULT_LABELS1,
) -> tuple[np.ndarray, list[str]]:
    """Считывает матрицу смежности графа с консоли (по Enter берётся матрица из задания 1 по умолчанию)."""
    print("Задание 1. Ввод матрицы смежности с консоли")
    print("По умолчанию используется матрица графа A, B, C, D из задания 1:")
    for row in default_matrix:
        print("  " + " ".join(str(x) for x in row))

    try:
        n_raw = input("Введите количество вершин n (или нажмите Enter для значения по умолчанию): ").strip()
    except EOFError:
        n_raw = ""

    if not n_raw:
        print("-> Выбрана матрица по умолчанию из задания 1.")
        return default_matrix.copy(), list(default_labels)

    n = int(n_raw)
    if n < 2:
        raise ValueError("Количество вершин должно быть не меньше 2.")

    use_row_defaults = n == default_matrix.shape[0]
    if use_row_defaults:
        print(f"Введите {n} строк по {n} чисел через пробел (пустая строка Enter — строка по умолчанию):")
    else:
        print(f"Введите {n} строк матрицы смежности (по {n} чисел через пробел):")

    rows = []
    for i in range(n):
        while True:
            default_hint = (
                f" [по умолчанию: {' '.join(map(str, default_matrix[i]))}]" if use_row_defaults else ""
            )
            try:
                line = input(f"Строка {i + 1}{default_hint}: ").strip()
            except EOFError:
                line = ""

            if not line and use_row_defaults:
                rows.append(default_matrix[i].astype(float).tolist())
                break

            nums = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+", line)]
            if len(nums) == n:
                rows.append(nums)
                break
            print(f"Ошибка: нужно ввести ровно {n} чисел. Повторите ввод строки {i + 1}.")

    A = np.array(rows, dtype=int if all(float(x).is_integer() for r in rows for x in r) else float)
    labels = [chr(ord("A") + i) if n <= 26 else str(i + 1) for i in range(n)]
    return A, labels


def solve_task1(A: np.ndarray, labels: list[str], save_path: str = "task1_graph.png", show_plot: bool = False) -> None:
    n = A.shape[0]
    D = np.diag(np.sum(A, axis=1))
    L = D - A

    print("\n" + "=" * 68)
    print("РЕЗУЛЬТАТЫ ПО ЗАДАНИЮ 1")
    print("=" * 68)
    print(f"Вершины графа: {', '.join(labels)}")
    print("\nМатрица смежности A:")
    print(A)
    print("\nМатрица степеней вершин D:")
    print(D)
    print("\nМатрица Кирхгофа (Лапласа) L = D - A:")
    print(L)

    coeffs = charpoly_coeffs(L)
    print("\n1) Уравнение для расчёта собственных значений det(L - λE) = 0:")
    print(format_det_matrix(L, "λ"))
    print("\n   Характеристическое уравнение:")
    print("   " + format_polynomial(coeffs, "λ"))

    # Для симметричной матрицы используем eigh (вещественный спектр), для общей — eig
    if np.allclose(L, L.T):
        eigvals, eigvecs = np.linalg.eigh(L)
        order = np.argsort(eigvals)
    else:
        eigvals, eigvecs = np.linalg.eig(L)
        order = np.lexsort((np.abs(eigvals.imag), eigvals.real))

    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    eigvals_clean = np.where(np.abs(eigvals) < 1e-10, 0.0, eigvals)

    fiedler_val = eigvals_clean[1]
    fiedler_vec = eigvecs[:, 1]
    # Фиксируем канонический знак вектора Фидлера для однозначного вывода
    nz = np.where(np.abs(fiedler_vec) > 1e-9)[0]
    if len(nz) > 0 and fiedler_vec[nz[0]].real < 0:
        fiedler_vec = -fiedler_vec
    fiedler_vec = np.where(np.abs(fiedler_vec) < 1e-10, 0.0, fiedler_vec)

    print("\n2) Собственные значения матрицы Кирхгофа (по возрастанию):")
    for idx, val in enumerate(eigvals_clean, 1):
        if np.isreal(val):
            print(f"   λ_{idx} = {float(np.real(val)):.4f}")
        else:
            print(f"   λ_{idx} = {val.real:.4f} {val.imag:+.4f}j")

    print(f"\n   Алгебраическая связность (число Фидлера): λ_2 = {np.real(fiedler_val):.4f}")
    print("   Вектор Фидлера v_2 (нормированный):")
    for lbl, comp in zip(labels, fiedler_vec):
        c_val = float(np.real(comp))
        print(f"     {lbl}: {c_val:+.4f}")

    # Масштабированный целочисленный/простой вид, если возможно
    min_nz = np.min(np.abs(np.real(fiedler_vec)[np.abs(np.real(fiedler_vec)) > 1e-6]))
    scaled_vec = np.real(fiedler_vec) / min_nz
    if np.allclose(scaled_vec, np.round(scaled_vec), atol=1e-4):
        int_vec = np.round(scaled_vec).astype(int)
        int_vec = np.where(int_vec == 0, 0, int_vec)
        print(f"   Вектор Фидлера без нормировки (пропорциональный): {int_vec.tolist()}")

    # Разбиение на кластеры по вектору Фидлера
    real_fv = np.real(fiedler_vec)
    cluster_pos = [labels[i] for i, v in enumerate(real_fv) if v > 1e-9]
    cluster_zero = [labels[i] for i, v in enumerate(real_fv) if abs(v) <= 1e-9]
    cluster_neg = [labels[i] for i, v in enumerate(real_fv) if v < -1e-9]

    print("\n   Разбиение графа на кластеры по вектору Фидлера:")
    if cluster_zero:
        c1_nonneg = [labels[i] for i, v in enumerate(real_fv) if v >= -1e-9]
        print(f"   - По порогу v_i >= 0: Кластер 1 = {c1_nonneg}, Кластер 2 = {cluster_neg}")
        print(f"   - С выделением пограничных вершин (v_i = 0): (+): {cluster_pos}, (0, мост): {cluster_zero}, (-): {cluster_neg}")
    else:
        print(f"   - Кластер 1 (v_i >= 0): {cluster_pos}")
        print(f"   - Кластер 2 (v_i < 0):  {cluster_neg}")

    # Отрисовка графа
    is_directed = not np.allclose(A, A.T)
    G = nx.from_numpy_array(A, create_using=nx.DiGraph if is_directed else nx.Graph)
    mapping = {i: labels[i] for i in range(n)}
    G = nx.relabel_nodes(G, mapping)

    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color="red", node_size=1100, edgecolors="#222222", linewidths=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=13, font_weight="bold", font_color="black", ax=ax)
    nx.draw_networkx_edges(G, pos, width=2.0, edge_color="#111111", ax=ax)
    ax.set_title("Задание 1: Граф A, B, C, D", fontsize=12, fontweight="bold", pad=14)
    ax.margins(0.22)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    print(f"\n   Рисунок графа сохранён в файл: {save_path}")
    if show_plot and "agg" not in plt.get_backend().lower():
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    A_mat, node_labels = read_adjacency_matrix_from_console()
    solve_task1(A_mat, node_labels, show_plot=True)
