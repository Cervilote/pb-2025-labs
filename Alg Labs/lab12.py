"""
Лабораторная работа №12
Движок 2D-геометрии для игровой платформы
"""

import math
import matplotlib.pyplot as plt


# =============================================================================
# Задание 1: Аффинные преобразования
# =============================================================================

def translate(points: list[tuple], tx: float, ty: float) -> list[tuple]:
    """
    Сдвиг точек на (tx, ty).

    Матрица преобразования:
    [[1, 0, 0],
     [0, 1, 0],
     [tx, ty, 1]]
    """
    return [(x + tx, y + ty) for x, y in points]


def rotate(points: list[tuple], angle_deg: float) -> list[tuple]:
    """
    Поворот точек вокруг начала координат на angle_deg градусов (против часовой).

    Матрица поворота:
    [[cos θ,  sin θ, 0],
     [-sin θ, cos θ, 0],
     [0,      0,     1]]
    """
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated = []
    for x, y in points:
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        rotated.append((new_x, new_y))

    return rotated


def scale(points: list[tuple], sx: float, sy: float) -> list[tuple]:
    """
    Масштабирование точек на (sx, sy).

    Матрица масштабирования:
    [[sx, 0,  0],
     [0,  sy, 0],
     [0,  0,  1]]
    """
    return [(x * sx, y * sy) for x, y in points]


def apply_transform_chain(points: list[tuple],
                          scale_factor: float = 1.0,
                          rotation_deg: float = 0.0,
                          translate_x: float = 0.0,
                          translate_y: float = 0.0) -> list[tuple]:
    """
    Применяет цепочку преобразований: scale -> rotate -> translate.

    Порядок важен! Мы применяем преобразования в указанном порядке.
    """
    result = points

    # 1. Масштабирование
    if scale_factor != 1.0:
        result = scale(result, scale_factor, scale_factor)

    # 2. Поворот
    if rotation_deg != 0.0:
        result = rotate(result, rotation_deg)

    # 3. Сдвиг
    if translate_x != 0.0 or translate_y != 0.0:
        result = translate(result, translate_x, translate_y)

    return result


# =============================================================================
# Задание 2: Выпуклая оболочка — алгоритм Джарвиса (Gift Wrapping)
# =============================================================================

def cross(o: tuple, a: tuple, b: tuple) -> float:
    """
    Векторное произведение (ориентация тройки точек O->A->B).

    cross(O, A, B) = (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x)

    > 0: против часовой (CCW)
    < 0: по часовой (CW)
    = 0: коллинеарные
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def jarvis_hull(points: list[tuple]) -> list[tuple]:
    """
    Алгоритм Джарвиса (Gift Wrapping) для построения выпуклой оболочки.

    Сложность: O(n * h), где h — число вершин оболочки.

    При коллинеарных точках выбирается наиболее дальняя от current,
    чтобы избежать лишних вершин на рёбрах оболочки.

    Args:
        points: список точек (x, y)

    Returns:
        вершины выпуклой оболочки в порядке CCW
    """
    if len(points) < 3:
        return list(points)

    # Найти самую левую точку (при равенстве — самую нижнюю)
    start_idx = 0
    for i in range(1, len(points)):
        if (points[i][0] < points[start_idx][0] or
                (points[i][0] == points[start_idx][0] and points[i][1] < points[start_idx][1])):
            start_idx = i

    start = points[start_idx]
    hull = [start]

    current = start
    while True:
        # Выбрать любую другую точку как кандидат
        next_point = None
        for i, p in enumerate(points):
            if p == current:
                continue
            if next_point is None:
                next_point = p
            else:
                c = cross(current, next_point, p)
                if c < 0:
                    # p находится левее (более CCW) — берём p
                    next_point = p
                elif c == 0:
                    # Коллинеарные точки — берём наиболее дальнюю
                    # Вычисляем расстояние от current
                    dist_next = (next_point[0] - current[0]) ** 2 + (next_point[1] - current[1]) ** 2
                    dist_p = (p[0] - current[0]) ** 2 + (p[1] - current[1]) ** 2
                    if dist_p > dist_next:
                        next_point = p

        if next_point is None:
            break

        current = next_point

        # Если вернулись к началу — оболочка замкнута
        if current == start:
            break

        hull.append(current)

    return hull


# =============================================================================
# Задание 3: Алгоритм Грэхема (Graham Scan)
# =============================================================================

def graham_hull(points: list[tuple]) -> list[tuple]:
    """
    Алгоритм Грэхема для построения выпуклой оболочки.

    Сложность: O(n log n) из-за сортировки.

    Args:
        points: список точек (x, y)

    Returns:
        вершины выпуклой оболочки в порядке CCW

    Стратегия при одинаковом угле:
        Оставляем точки в порядке увеличения расстояния от pivot.
        Ближние точки first — это гарантирует, что дальние точки
        будут обработаны корректно и не создадут лишних вершин.
    """
    if len(points) < 3:
        return list(points)

    # Найти опорную точку (нижняя левая: min y, при равентсве — min x)
    pivot_idx = 0
    for i in range(1, len(points)):
        if (points[i][1] < points[pivot_idx][1] or
                (points[i][1] == points[pivot_idx][1] and points[i][0] < points[pivot_idx][0])):
            pivot_idx = i

    pivot = points[pivot_idx]

    # Создать список остальных точек
    other_points = [p for i, p in enumerate(points) if i != pivot_idx]

    # Сортировка по полярному углу относительно pivot
    # Используем atan2 для простоты
    def polar_angle(p):
        return math.atan2(p[1] - pivot[1], p[0] - pivot[0])

    def distance(p):
        return (p[0] - pivot[0]) ** 2 + (p[1] - pivot[1]) ** 2

    # Сортировка: сначала по углу, затем по расстоянию (ближние first)
    other_points.sort(key=lambda p: (polar_angle(p), distance(p)))

    # Удалить коллинеарные точки, оставляя только самую дальнюю в каждом направлении
    # Это оптимизирует оболочку
    filtered = []
    for p in other_points:
        if not filtered:
            filtered.append(p)
        else:
            # Проверяем коллинеарность с последней точкой
            last = filtered[-1]
            angle1 = polar_angle(last)
            angle2 = polar_angle(p)
            if abs(angle1 - angle2) < 1e-10:
                # Коллинеарные — оставляем только дальнюю
                if distance(p) > distance(last):
                    filtered[-1] = p
            else:
                filtered.append(p)

    # Инициализировать стек
    stack = [pivot]
    if filtered:
        stack.append(filtered[0])

    # Обработка остальных точек
    for i in range(1, len(filtered)):
        p = filtered[i]

        # Откатываемся, пока не получим левый поворот (CCW)
        while len(stack) >= 2:
            o = stack[-2]
            a = stack[-1]
            if cross(o, a, p) <= 0:
                stack.pop()
            else:
                break

        stack.append(p)

    return stack


def sets_match(hull1: list[tuple], hull2: list[tuple]) -> bool:
    """Проверяет совпадение наборов вершин (без учёта порядка)."""

    def normalize(hull):
        # Сортируем для сравнения
        return tuple(sorted([(round(x, 10), round(y, 10)) for x, y in hull]))

    return normalize(hull1) == normalize(hull2)


# =============================================================================
# Визуализация
# =============================================================================

def visualize_hull(points: list[tuple], hull: list[tuple], filename: str = "convex_hull.png"):
    """
    Визуализирует точки и выпуклую оболочку.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Исходные точки — синие
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.scatter(xs, ys, c='blue', s=50, label='Input points', zorder=5)

    # Вершины оболочки — красные маркеры
    hx = [p[0] for p in hull]
    hy = [p[1] for p in hull]
    ax.scatter(hx, hy, c='red', s=100, marker='s', label='Hull vertices', zorder=6)

    # Рёбра оболочки — замкнутая красная линия
    hull_closed = hull + [hull[0]]  # Замыкаем контур
    hx_closed = [p[0] for p in hull_closed]
    hy_closed = [p[1] for p in hull_closed]
    ax.plot(hx_closed, hy_closed, 'r-', linewidth=2, label='Hull edges', zorder=4)

    # Подписи вершин
    for i, (x, y) in enumerate(hull):
        ax.annotate(f'{i + 1}', (x, y), textcoords="offset points",
                    xytext=(5, 5), fontsize=12, color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Convex Hull')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig(filename)
    print(f"Визуализация сохранена в {filename}")
    plt.close()


def visualize_comparison(points: list[tuple], hull1: list[tuple],
                         hull2: list[tuple], filename: str = "hull_comparison.png"):
    """
    Визуализирует сравнение двух алгоритмов.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Исходные точки — серые
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.scatter(xs, ys, c='gray', s=50, alpha=0.5, label='Input points', zorder=3)

    # Оболочка Джарвиса — синяя
    jx = [p[0] for p in hull1] + [hull1[0][0]]
    jy = [p[1] for p in hull1] + [hull1[0][1]]
    ax.plot(jx, jy, 'b-', linewidth=2, label='Jarvis March', zorder=4)

    # Оболочка Грэхема — зелёная
    gx = [p[0] for p in hull2] + [hull2[0][0]]
    gy = [p[1] for p in hull2] + [hull2[0][1]]
    ax.plot(gx, gy, 'g--', linewidth=2, label='Graham Scan', zorder=4)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Convex Hull Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig(filename)
    print(f"Сравнение сохранено в {filename}")
    plt.close()


# =============================================================================
# Главная функция — демонстрация всех заданий
# =============================================================================

def main():
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №12: Движок 2D-геометрии")
    print("=" * 70)

    # =============================================================================
    # Задание 1: Аффинные преобразования
    # =============================================================================
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 1: Аффинные преобразования")
    print("=" * 70)

    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    print(f"\nOriginal: {square}")

    # 1. Масштабирование в 1.5 раза
    scaled = scale(square, 1.5, 1.5)
    print("\nAfter scale(1.5, 1.5):")
    print(f"  {[tuple(round(x, 4) for x in p) for p in scaled]}")

    # 2. Поворот на 45°
    rotated = rotate(scaled, 45)
    print("\nAfter rotate(45°):")
    print(f"  {[tuple(round(x, 4) for x in p) for p in rotated]}")

    # 3. Сдвиг на (5, 3)
    translated = translate(rotated, 5, 3)
    print("\nAfter translate(5, 3):")
    print(f"  {[tuple(round(x, 4) for x in p) for p in translated]}")

    # Демонстрация отдельных функций
    print("\n--- Демонстрация отдельных преобразований ---")

    triangle = [(1, 1), (3, 1), (2, 3)]
    print(f"Треугольник: {triangle}")

    scaled_tri = scale(triangle, 2, 0.5)
    print(f"После scale(2, 0.5): {scaled_tri}")

    rotated_tri = rotate(scaled_tri, 90)
    print(f"После rotate(90°): {[tuple(round(x, 4) for x in p) for p in rotated_tri]}")

    translated_tri = translate(rotated_tri, -2, 1)
    print(f"После translate(-2, 1): {[tuple(round(x, 4) for x in p) for p in translated_tri]}")

    # =============================================================================
    # Задание 2: Алгоритм Джарвиса
    # =============================================================================
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 2: Алгоритм Джарвиса (Gift Wrapping)")
    print("=" * 70)

    points = [(0, 0), (2, 0), (4, 0), (4, 4), (2, 4), (0, 4), (0, 2), (1, 2), (2, 1), (3, 3)]
    print(f"\nInput points ({len(points)}): {points}")

    jarvis_result = jarvis_hull(points)
    print(f"\nJarvis hull ({len(jarvis_result)} vertices): {jarvis_result}")

    # Тест с коллинеарными точками
    collinear_points = [(0, 0), (1, 1), (2, 2), (3, 0), (0, 3)]
    print(f"\nТест с коллинеарными точками: {collinear_points}")
    collinear_hull = jarvis_hull(collinear_points)
    print(f"Jarvis hull: {collinear_hull}")

    # =============================================================================
    # Задание 3: Алгоритм Грэхема
    # =============================================================================
    print("\n" + "=" * 70)
    print("ЗАДАНИЕ 3: Алгоритм Грэхема (Graham Scan)")
    print("=" * 70)

    graham_result = graham_hull(points)
    print(f"\nGraham hull ({len(graham_result)} vertices): {graham_result}")

    # Сравнение результатов
    print("\n--- Сравнение алгоритмов ---")
    print(f"Points: {points}")
    print(f"Jarvis hull  ({len(jarvis_result)} vertices): {jarvis_result}")
    print(f"Graham hull  ({len(graham_result)} vertices): {graham_result}")
    print(f"Vertex sets match: {sets_match(jarvis_result, graham_result)}")

    # Тест Грэхема с коллинеарными
    graham_collinear = graham_hull(collinear_points)
    print(f"\nТест Грэхема с коллинеарными точками: {collinear_points}")
    print(f"Graham hull: {graham_collinear}")

    # =============================================================================
    # Визуализация
    # =============================================================================
    print("\n" + "=" * 70)
    print("ВИЗУАЛИЗАЦИЯ")
    print("=" * 70)

    visualize_hull(points, graham_result, "convex_hull.png")
    visualize_comparison(points, jarvis_result, graham_result, "hull_comparison.png")

    print("\n" + "=" * 70)
    print("Все задания выполнены!")
    print("=" * 70)


if __name__ == "__main__":
    main()