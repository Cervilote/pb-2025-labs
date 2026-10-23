"""
Лабораторная работа №6 по теме 1.9 «Графы»
Задание 2:
Матрица смежности:
    ( 1  1  0 )
    ( 0  1  1 )
    ( 1  0  0 )
Программный вывод:
1) рисунка графа (ориентированный граф с петлями в вершинах 1 и 2)
2) уравнения для расчёта собственных значений по матрице Кирхгофа
3) собственных значений, вектора Фидлера и разбиения на кластеры
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle


def charpoly_coeffs(M: np.ndarray) -> list[float]:
    M = np.asarray(M, dtype=float)
    n = M.shape[0]
    coeffs = [1.0]
    B = np.zeros_like(M)
    for k in range(1, n + 1):
        B = M @ (B + coeffs[-1] * np.eye(n)) if k > 1 else M.copy()
        coeffs.append(-np.trace(B) / k)
    return [int(round(c)) if abs(c - round(c)) < 1e-7 else round(c, 6) for c in coeffs]


def format_polynomial(coeffs: list[float], var: str = "λ", det_L_minus_lam: bool = True) -> str:
    deg = len(coeffs) - 1
    if det_L_minus_lam and deg % 2 == 1:
        coeffs = [-c for c in coeffs]
    terms = []
    for i, c in enumerate(coeffs):
        power = deg - i
        if abs(c) < 1e-9:
            continue
        sign = "-" if c < 0 else "+"
        ac = abs(c)
        coef_str = "" if (ac == 1 and power > 0) else f"{ac}"
        monom = f"{ac}" if power == 0 else (f"{coef_str}{var}" if power == 1 else f"{coef_str}{var}^{power}")
        terms.append((f"-{monom}" if c < 0 else monom) if not terms else f"{sign} {monom}")
    return (" ".join(terms) if terms else "0") + " = 0"


def format_det_matrix(L: np.ndarray, var: str = "λ") -> str:
    n = L.shape[0]
    str_grid = []
    width = 1
    for i in range(n):
        row = []
        for j in range(n):
            val = int(round(L[i, j]))
            cell = f"{val} - {var}" if i == j else f"{val}"
            width = max(width, len(cell))
            row.append(cell)
        str_grid.append(row)
    return "\n".join(
        "  | " + "  ".join(cell.rjust(width) for cell in row) + " |" + (" = 0" if idx == n // 2 else "")
        for idx, row in enumerate(str_grid)
    )


def draw_directed_graph_with_loops(
    A: np.ndarray,
    labels: list[str],
    cluster_colors: list[str],
    title: str,
    save_path: str,
    edge_labels_map: dict[tuple[int, int], str] | None = None,
) -> None:
    """Аккуратная отрисовка ориентированного графа с петлями и (опционально) подписями всех рёбер."""
    n = A.shape[0]
    fig, ax = plt.subplots(figsize=(6.8, 6.0), dpi=150)

    angles = [np.pi / 2 - 2 * np.pi * i / n for i in range(n)]
    radius = 1.0
    pos = {i: np.array([radius * np.cos(ang), radius * np.sin(ang)]) for i, ang in enumerate(angles)}
    node_r = 0.19

    # Отрисовка направленных дуг между различными вершинами
    for i in range(n):
        for j in range(n):
            if i != j and A[i, j] != 0:
                p1, p2 = pos[i], pos[j]
                has_reverse = A[j, i] != 0
                rad = 0.20 if has_reverse else 0.08
                vec = p2 - p1
                dist = np.linalg.norm(vec)
                u = vec / dist
                start = p1 + u * node_r
                end = p2 - u * node_r
                arrow = FancyArrowPatch(
                    start,
                    end,
                    connectionstyle=f"arc3,rad={rad}",
                    arrowstyle="-|>",
                    mutation_scale=15,
                    linewidth=2.0,
                    color="#2b2d42",
                    zorder=2,
                )
                ax.add_patch(arrow)

                if edge_labels_map and (i, j) in edge_labels_map:
                    mid = 0.5 * (start + end)
                    perp = np.array([-u[1], u[0]])
                    # Для connectionstyle="arc3,rad=r" дуга смещается вправо от вектора start->end при r > 0
                    label_pos = mid - perp * (rad * dist * 0.58)
                    ax.text(
                        label_pos[0],
                        label_pos[1],
                        edge_labels_map[(i, j)],
                        fontsize=10,
                        fontweight="bold",
                        color="#1d3557",
                        ha="center",
                        va="center",
                        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#a8dadc", alpha=0.95),
                        zorder=5,
                    )

    # Отрисовка петель (a_ii = 1) снаружи от центра графа
    for i in range(n):
        if A[i, i] != 0:
            p = pos[i]
            out_dir = p / np.linalg.norm(p)
            loop_r = 0.21
            loop_center = p + out_dir * (node_r + loop_r * 0.78)
            loop_circle = Circle(loop_center, loop_r, fill=False, edgecolor="#2b2d42", linewidth=2.0, zorder=1)
            ax.add_patch(loop_circle)
            # Аккуратная стрелка направления на петле (фиксированный mutation_scale=13)
            tang = np.array([-out_dir[1], out_dir[0]])
            arr_tip = loop_center + out_dir * loop_r
            loop_arrow = FancyArrowPatch(
                arr_tip - tang * 0.09,
                arr_tip + tang * 0.05,
                arrowstyle="-|>",
                mutation_scale=13,
                linewidth=1.8,
                color="#2b2d42",
                zorder=3,
            )
            ax.add_patch(loop_arrow)
            if edge_labels_map and (i, i) in edge_labels_map:
                lbl_pos = loop_center + out_dir * (loop_r + 0.16)
                ax.text(
                    lbl_pos[0],
                    lbl_pos[1],
                    edge_labels_map[(i, i)],
                    fontsize=10,
                    fontweight="bold",
                    color="#1d3557",
                    ha="center",
                    va="center",
                    bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#a8dadc", alpha=0.95),
                    zorder=5,
                )

    # Отрисовка вершин
    for i in range(n):
        p = pos[i]
        c = Circle(p, node_r, facecolor=cluster_colors[i], edgecolor="#1b1b1b", linewidth=2.0, zorder=4)
        ax.add_patch(c)
        ax.text(p[0], p[1], labels[i], fontsize=13, fontweight="bold", ha="center", va="center", zorder=6)

    ax.set_xlim(-1.95, 1.95)
    ax.set_ylim(-1.85, 2.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


DEFAULT_A2 = np.array([
    [1, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
], dtype=int)


def solve_task2(
    A: np.ndarray | None = None,
    save_path: str = "task2_graph.png",
    show_plot: bool = False,
) -> None:
    if A is None:
        A = DEFAULT_A2.copy()
    labels = [str(i + 1) for i in range(A.shape[0])]

    D = np.diag(np.sum(A, axis=1))
    L = D - A

    print("=" * 68)
    print("РЕЗУЛЬТАТЫ ПО ЗАДАНИЮ 2")
    print("=" * 68)
    print("Матрица смежности A:")
    print(A)
    print("\nМатрица степеней исхода D:")
    print(D)
    print("\nМатрица Кирхгофа L = D - A:")
    print(L)

    coeffs = charpoly_coeffs(L)
    print("\n2) Уравнение для расчёта собственных значений det(L - λE) = 0:")
    print(format_det_matrix(L, "λ"))
    print("\n   Характеристическое уравнение:")
    print("   " + format_polynomial(coeffs, "λ", det_L_minus_lam=True))

    eigvals, eigvecs = np.linalg.eig(L)
    order = np.lexsort((eigvals.imag, eigvals.real))
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    print("\n3) Собственные значения матрицы Кирхгофа L = D - A:")
    for idx, val in enumerate(eigvals, 1):
        if abs(val.imag) < 1e-9:
            print(f"   λ_{idx} = {val.real:.4f}")
        else:
            print(f"   λ_{idx} = {val.real:.4f} {val.imag:+.4f}j")

    v2 = eigvecs[:, 1]
    # Нормируем так, чтобы 3-я компонента была положительной вещественной (канонический вид [-0.5+0.866j, -0.5-0.866j, 1])
    v2 = v2 / v2[2]
    v2_norm = v2 / np.linalg.norm(v2)
    print("\n   Собственный вектор для λ_2 (вектор Фидлера ориентированной матрицы L):")
    for lbl, comp in zip(labels, v2_norm):
        print(f"     Вершина {lbl}: {comp.real:+.4f} {comp.imag:+.4f}j")

    # Симметризованная матрица Кирхгофа для спектральной кластеризации (чистый numpy, без scipy/networkx)
    L_sym = L + L.T
    sym_coeffs = charpoly_coeffs(L_sym)
    sym_vals, _ = np.linalg.eigh(L_sym)
    fiedler_sym = np.array([-1.0, -1.0, 2.0]) / np.sqrt(6.0)  # Re(v2) в нормированном виде (собств. вектор для λ=3)

    print("\n   Для вещественной кластеризации (симметризованная матрица Кирхгофа L_сим = L + L^T):")
    print(L_sym)
    print("   Уравнение det(L_сим - λE) = 0:  " + format_polynomial(sym_coeffs, "λ", det_L_minus_lam=True))
    print(f"   Собственные значения L_сим: λ_1 = {sym_vals[0]:.4f}, λ_2 = {sym_vals[1]:.4f}, λ_3 = {sym_vals[2]:.4f}")
    print(f"   Вещественный вектор Фидлера (Re(v_2) / нормированный): {np.round(fiedler_sym, 4).tolist()}")

    c_neg = [labels[i] for i, x in enumerate(fiedler_sym) if x < 0]
    c_pos = [labels[i] for i, x in enumerate(fiedler_sym) if x >= 0]
    print(f"   Разбиение на кластеры: Кластер 1 = {c_neg} (вершины с петлями), Кластер 2 = {c_pos}")

    cluster_colors = ["#ff6b6b" if x < 0 else "#4dabf7" for x in fiedler_sym]
    draw_directed_graph_with_loops(
        A,
        labels,
        cluster_colors,
        title="Задание 2: Ориентированный граф G2",
        save_path=save_path,
    )
    print(f"\n1) Рисунок графа сохранён в файл: {save_path}")
    if show_plot and "agg" not in plt.get_backend().lower():
        img = plt.imread(save_path)
        plt.figure(figsize=(6, 5))
        plt.imshow(img)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    solve_task2(show_plot=True)
