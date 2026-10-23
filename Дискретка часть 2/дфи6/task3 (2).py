"""
Лабораторная работа №6 по теме 1.9 «Графы»
Задание 3:
Матрица смежности:
    ( 1  1  1 )
    ( 1  1  1 )
    ( 1  0  1 )
Программный вывод:
1) спектра графа и рисунка графа с введёнными обозначениями рёбер (e1..e8)
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


def format_polynomial(coeffs: list[float], var: str = "λ", det_M_minus_var: bool = True) -> str:
    deg = len(coeffs) - 1
    if det_M_minus_var and deg % 2 == 1:
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


def format_det_matrix(M: np.ndarray, var: str = "λ") -> str:
    n = M.shape[0]
    str_grid = []
    width = 1
    for i in range(n):
        row = []
        for j in range(n):
            val = int(round(M[i, j]))
            cell = f"{val} - {var}" if i == j else f"{val}"
            width = max(width, len(cell))
            row.append(cell)
        str_grid.append(row)
    return "\n".join(
        "  | " + "  ".join(cell.rjust(width) for cell in row) + " |" + (" = 0" if idx == n // 2 else "")
        for idx, row in enumerate(str_grid)
    )


def plot_task3_graph_and_spectrum(
    A: np.ndarray,
    labels: list[str],
    edge_labels_map: dict[tuple[int, int], str],
    adj_eigs: np.ndarray,
    lap_eigs: np.ndarray,
    fiedler_vec: np.ndarray,
    save_path: str,
) -> None:
    """Строит граф с подписями рёбер e1..e8 и диаграмму спектра графа на одном рисунке."""
    n = A.shape[0]
    fig, (ax, ax_spec) = plt.subplots(1, 2, figsize=(12.2, 5.8), dpi=150, gridspec_kw={"width_ratios": [1.3, 1.0]})

    angles = [np.pi / 2 - 2 * np.pi * i / n for i in range(n)]
    radius = 1.0
    pos = {i: np.array([radius * np.cos(ang), radius * np.sin(ang)]) for i, ang in enumerate(angles)}
    node_r = 0.19

    # Направленные дуги между разными вершинами
    for i in range(n):
        for j in range(n):
            if i != j and A[i, j] != 0:
                p1, p2 = pos[i], pos[j]
                has_reverse = A[j, i] != 0
                rad = 0.22 if has_reverse else 0.10
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

                mid = 0.5 * (start + end)
                perp = np.array([-u[1], u[0]])
                label_pos = mid - perp * (rad * dist * 0.62)
                ax.text(
                    label_pos[0],
                    label_pos[1],
                    edge_labels_map[(i, j)],
                    fontsize=9.5,
                    fontweight="bold",
                    color="#1d3557",
                    ha="center",
                    va="center",
                    bbox=dict(boxstyle="round,pad=0.20", facecolor="#f8f9fa", edgecolor="#457b9d", alpha=0.96),
                    zorder=5,
                )

    # Петли с подписями
    for i in range(n):
        if A[i, i] != 0:
            p = pos[i]
            out_dir = p / np.linalg.norm(p)
            loop_r = 0.21
            loop_center = p + out_dir * (node_r + loop_r * 0.78)
            ax.add_patch(Circle(loop_center, loop_r, fill=False, edgecolor="#2b2d42", linewidth=2.0, zorder=1))
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
            lbl_pos = loop_center + out_dir * (loop_r + 0.19)
            ax.text(
                lbl_pos[0],
                lbl_pos[1],
                edge_labels_map[(i, i)],
                fontsize=9.5,
                fontweight="bold",
                color="#1d3557",
                ha="center",
                va="center",
                bbox=dict(boxstyle="round,pad=0.20", facecolor="#f8f9fa", edgecolor="#457b9d", alpha=0.96),
                zorder=5,
            )

    # Вершины
    cluster_colors = ["#ff6b6b" if x > 0 else "#4dabf7" for x in fiedler_vec]
    for i in range(n):
        p = pos[i]
        ax.add_patch(Circle(p, node_r, facecolor=cluster_colors[i], edgecolor="#1b1b1b", linewidth=2.0, zorder=4))
        ax.text(p[0], p[1], labels[i], fontsize=13, fontweight="bold", ha="center", va="center", zorder=6)

    ax.set_xlim(-2.05, 2.05)
    ax.set_ylim(-1.90, 2.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Задание 3: Граф G3 с обозначением рёбер (e1–e8)", fontsize=11.5, fontweight="bold")

    # Правая панель: Спектр матрицы смежности A и спектр матрицы Кирхгофа L
    x_idx = np.arange(1, n + 1)
    width = 0.34
    bars1 = ax_spec.bar(x_idx - width / 2, adj_eigs, width, label="Спектр графа Spec(A)", color="#457b9d", edgecolor="#1d3557")
    bars2 = ax_spec.bar(x_idx + width / 2, lap_eigs, width, label="Спектр Кирхгофа Spec(L)", color="#e76f51", edgecolor="#6b2c1a")
    ax_spec.axhline(0, color="#333333", linewidth=0.9)
    ax_spec.set_xticks(x_idx)
    ax_spec.set_xticklabels([f"i = {k}" for k in x_idx], fontsize=10)
    ax_spec.set_ylabel("Собственные значения", fontsize=10)
    ax_spec.set_title("Спектр графа и матрицы Кирхгофа", fontsize=11.5, fontweight="bold")
    ax_spec.grid(axis="y", linestyle="--", alpha=0.45)
    ax_spec.legend(fontsize=9.5, loc="upper left")
    ax_spec.set_ylim(-0.3, max(np.max(adj_eigs), np.max(lap_eigs)) + 0.65)

    for b in list(bars1) + list(bars2):
        h = b.get_height()
        ax_spec.text(
            b.get_x() + b.get_width() / 2,
            h + 0.08,
            f"{h:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


DEFAULT_A3 = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 0, 1],
], dtype=int)


def solve_task3(
    A: np.ndarray | None = None,
    save_path: str = "task3_graph.png",
    show_plot: bool = False,
) -> None:
    if A is None:
        A = DEFAULT_A3.copy()
    labels = [str(i + 1) for i in range(A.shape[0])]

    # 1) Обозначение всех рёбер/дуг графа e1..e8
    edge_labels_map: dict[tuple[int, int], str] = {}
    edge_idx = 1
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i, j] != 0:
                edge_labels_map[(i, j)] = f"e{edge_idx}"
                edge_idx += 1

    print("=" * 68)
    print("РЕЗУЛЬТАТЫ ПО ЗАДАНИЮ 3")
    print("=" * 68)
    print("Матрица смежности A:")
    print(A)

    print("\n1) Обозначение рёбер (дуг) графа:")
    for (u, v), ename in edge_labels_map.items():
        kind = "петля" if u == v else "дуга"
        print(f"   {ename}: ({labels[u]} -> {labels[v]}) [{kind}]")

    # Спектр графа (собственные значения матрицы смежности A)
    adj_coeffs = charpoly_coeffs(A)
    adj_eigs = np.sort(np.real_if_close(np.linalg.eigvals(A)).real)
    adj_eigs = np.where(np.abs(adj_eigs) < 1e-10, 0.0, adj_eigs)

    print("\n   Спектр графа Spec(A) (собственные значения матрицы смежности det(A - μE) = 0):")
    print("   Уравнение: " + format_polynomial(adj_coeffs, "μ", det_M_minus_var=True))
    print("   Собственные значения матрицы смежности A: " + ", ".join(f"μ_{i+1} = {v:.4f}" for i, v in enumerate(adj_eigs)))

    # 2) Матрица Кирхгофа L = D - A и характеристическое уравнение
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    lap_coeffs = charpoly_coeffs(L)

    print("\nМатрица степеней исхода D:")
    print(D)
    print("\nМатрица Кирхгофа L = D - A:")
    print(L)

    print("\n2) Уравнение для расчёта собственных значений по матрице Кирхгофа det(L - λE) = 0:")
    print(format_det_matrix(L, "λ"))
    print("\n   Характеристическое уравнение:")
    print("   " + format_polynomial(lap_coeffs, "λ", det_M_minus_var=True))

    # 3) Собственные значения и вектор Фидлера
    eigvals, eigvecs = np.linalg.eig(L)
    order = np.argsort(eigvals.real)
    eigvals = np.real_if_close(eigvals[order]).real
    eigvecs = np.real_if_close(eigvecs[:, order]).real
    eigvals = np.where(np.abs(eigvals) < 1e-10, 0.0, eigvals)

    fiedler_val = eigvals[1]
    fiedler_vec = eigvecs[:, 1]
    if fiedler_vec[0] < 0:
        fiedler_vec = -fiedler_vec
    fiedler_vec = np.where(np.abs(fiedler_vec) < 1e-10, 0.0, fiedler_vec)

    print("\n3) Собственные значения матрицы Кирхгофа L:")
    for idx, val in enumerate(eigvals, 1):
        print(f"   λ_{idx} = {val:.4f}")

    print(f"\n   Алгебраическая связность (число Фидлера): λ_2 = {fiedler_val:.4f}")
    print("   Вектор Фидлера v_2 (нормированный):")
    for lbl, comp in zip(labels, fiedler_vec):
        print(f"     Вершина {lbl}: {comp:+.4f}")

    scaled = np.round(fiedler_vec / np.min(np.abs(fiedler_vec[np.abs(fiedler_vec) > 1e-6]))).astype(int)
    print(f"   Вектор Фидлера в целом виде (без нормировки): {scaled.tolist()}")

    cluster_1 = [labels[i] for i, v in enumerate(fiedler_vec) if v >= 0]
    cluster_2 = [labels[i] for i, v in enumerate(fiedler_vec) if v < 0]
    print(f"\n   Разбиение графа на кластеры по вектору Фидлера:")
    print(f"   - Кластер 1 (v_i >= 0): {cluster_1}")
    print(f"   - Кластер 2 (v_i < 0):  {cluster_2}")

    plot_task3_graph_and_spectrum(
        A=A,
        labels=labels,
        edge_labels_map=edge_labels_map,
        adj_eigs=adj_eigs,
        lap_eigs=eigvals,
        fiedler_vec=fiedler_vec,
        save_path=save_path,
    )
    print(f"\n   Рисунок графа с обозначением рёбер и спектром сохранён в файл: {save_path}")
    if show_plot and "agg" not in plt.get_backend().lower():
        img = plt.imread(save_path)
        plt.figure(figsize=(10, 5))
        plt.imshow(img)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    solve_task3(show_plot=True)
