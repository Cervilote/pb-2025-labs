# -*- coding: utf-8 -*-
"""
Задание №2. Аналитическая функция tan(x) без математической библиотеки.

Разрешённые операции для вычисления самой функции: только + - * / и
целые числа (коэффициенты/факториалы ряда Тейлора). Функции sin/cos/exp/
tan из math для my_tan НЕ используются. math используется ТОЛЬКО в
тестах для сравнения (math.tan, math.pi для проверки, time для замера).

Идея:
    tan(x) = sin(x) / cos(x)

    sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ...
    cos(x) = 1 - x^2/2! + x^4/4! - x^6/6! + ...

    + редукция аргумента к [-pi/4, pi/4], где ряд сходится за ~9-11 членов.
"""

import math  # ТОЛЬКО для сравнения в тестах, НЕ внутри my_tan
import time

# pi с точностью double (константа, а не вычисление функции)
PI = 3.14159265358979323846264338327950288
HALF_PI = PI / 2
QUARTER_PI = PI / 4

# Порог машинной точности double: дальше члены ряда не меняют сумму
EPS = 2.220446049250313e-16  # 2^-52


def _sin_cos_taylor(x):
    """
    Одновременно вычисляет sin(x) и cos(x) рядами Тейлора для |x| <= pi/4.
    Используются только + - * / и целые числа.

    Члены ряда получаются рекуррентно, без pow и факториалов:
        sin:  term_1 = x,        term_{n} = term_{n-1} * (-x^2) / ((2n)(2n+1))
        cos:  term_0 = 1,        term_{n} = term_{n-1} * (-x^2) / ((2n-1)(2n))
    Так каждый следующий член стоит 2 умножения и 1 деление.

    Критерий остановки (эффективность + максимальная точность):
    останавливаемся, только когда очередной член уже не изменяет сумму
    в арифметике double (s + term == s) или |term| < EPS * |s|.
    Раньше остановиться нельзя без потери точности, позже - бессмысленно.
    Возвращает (sin, cos, число_членов).
    """
    x2 = x * x

    # --- sin ---
    sin_sum = x
    term = x
    n = 1
    sin_terms = 1
    while True:
        # переход к следующему нечётному члену: знаменатель (2n)(2n+1)
        term = term * (-x2) / ((2 * n) * (2 * n + 1))
        new_sum = sin_sum + term
        sin_terms += 1
        if new_sum == sin_sum or abs(term) < EPS * abs(sin_sum):
            sin_sum = new_sum
            break
        sin_sum = new_sum
        n += 1
        if n > 100:  # страховка, на практике недостижима при |x|<=pi/4
            break

    # --- cos ---
    cos_sum = 1.0
    term = 1.0
    n = 1
    cos_terms = 1
    while True:
        term = term * (-x2) / ((2 * n - 1) * (2 * n))
        new_sum = cos_sum + term
        cos_terms += 1
        if new_sum == cos_sum or abs(term) < EPS * abs(cos_sum):
            cos_sum = new_sum
            break
        cos_sum = new_sum
        n += 1
        if n > 100:
            break

    return sin_sum, cos_sum, sin_terms + cos_terms


def my_tan(x):
    """
    Аналитическая функция tan(x), вычисленная только операциями + - * /
    и целыми числами (плюс константа pi).

    Шаги:
    1) Редукция по периоду: tan(x + k*pi) = tan(x).
       k = округление x/pi к ближайшему целому, x := x - k*pi.
       Теперь |x| <= pi/2.
    2) Редукция к четверти: если |x| > pi/4, используем
       tan(x) = sign / tan(pi/2 - |x|), аргумент становится <= pi/4.
       Около полюсов x = pi/2 + k*pi это даёт малый аргумент для
       знаменателя и tan корректно уходит в +-бесконечность по модулю.
    3) sin и cos - рядами Тейлора, tan = sin/cos.
    """
    if x != x:            # NaN
        return float("nan")
    if x == float("inf") or x == float("-inf"):
        return float("nan")  # как math.tan: у tan(inf) значение не определено

    # 1) Редукция по периоду pi. int() отбрасывает дробную часть к нулю,
    #    поэтому прибавляем/вычитаем 0.5 для округления к ближайшему целому.
    if x >= 0:
        k = int(x / PI + 0.5)
    else:
        k = int(x / PI - 0.5)
    x = x - k * PI  # теперь -pi/2 <= x <= pi/2

    # 2) Редукция к [-pi/4, pi/4]
    sign = 1.0
    invert = False
    if x < 0:
        sign = -1.0
        x = -x
    if x > QUARTER_PI:
        x = HALF_PI - x  # 0 <= x < pi/4, а tan(исходный) = 1/tan(новый)
        invert = True

    # 3) Ряды Тейлора
    s, c, _ = _sin_cos_taylor(x)

    if invert:
        # tan = cos/sin для дополняющего угла; при x->0 это полюс
        if s == 0.0:
            return sign * float("inf")
        return sign * (c / s)
    if c == 0.0:
        return sign * float("inf")
    return sign * (s / c)


def my_tan_counted(x):
    """Та же функция, но возвращает ещё и число сложенных членов ряда
    (для демонстрации эффективности). Логика повторяет my_tan."""
    if x >= 0:
        k = int(x / PI + 0.5)
    else:
        k = int(x / PI - 0.5)
    x = x - k * PI
    sign = 1.0
    invert = False
    if x < 0:
        sign = -1.0
        x = -x
    if x > QUARTER_PI:
        x = HALF_PI - x
        invert = True
    s, c, terms = _sin_cos_taylor(x)
    if invert:
        return sign * (c / s), terms
    return sign * (s / c), terms


def test(num_points=1000):
    print("=" * 78)
    print("Сравнение my_tan (ряд Тейлора, только + - * /) с math.tan")
    print("=" * 78)

    # Основная числовая ось: 1000 точек на [-1.45, 1.45]
    # (до полюсов +-pi/2 ~= +-1.5708 не доходим, там tan -> inf)
    xs = [-1.45 + 2.90 * i / (num_points - 1) for i in range(num_points)]

    max_abs_err = 0.0
    max_rel_err = 0.0
    worst_x = 0.0
    total_terms = 0
    first_mismatch = None  # первая точка, где my_tan != math.tan точно (по битам)
    mismatch_count = 0     # сколько всего точек не совпало точно

    print(f"\n{'x':>12} {'my_tan':>22} {'math.tan':>22} {'|разность|':>14}")
    print("-" * 78)
    for i, x in enumerate(xs):
        mine, terms = my_tan_counted(x)
        total_terms += terms
        ref = math.tan(x)
        abs_err = abs(mine - ref)
        rel_err = abs_err / abs(ref) if ref != 0 else abs_err
        if abs_err > max_abs_err:
            max_abs_err = abs_err
            worst_x = x
        if rel_err > max_rel_err:
            max_rel_err = rel_err
        if mine != ref:  # точное (побитовое) несовпадение значений float
            mismatch_count += 1
            if first_mismatch is None:
                first_mismatch = (i, x, mine, ref, abs_err)
        if i < 10 or i >= num_points - 3:  # печатаем края таблицы
            print(f"{x:12.6f} {mine:22.15f} {ref:22.15f} {abs_err:14.3e}")
        elif i == 10:
            print(f"{'...':>12} {'...':>22} {'...':>22} {'...':>14}")

    print("-" * 78)
    print(f"Точек проверено:                 {num_points}")
    print(f"Макс. абсолютная ошибка:         {max_abs_err:.3e}  (при x = {worst_x:.6f})")
    print(f"Макс. относительная ошибка:     {max_rel_err:.3e}")
    print(f"Среднее число членов ряда:       {total_terms / num_points:.1f} (sin+cos вместе)")
    print(f"Точность double (1 ulp ~ EPS):   {EPS:.3e}")
    if first_mismatch is not None:
        i, x, mine, ref, abs_err = first_mismatch
        print("\nПервое точное несовпадение с math.tan:")
        print(f"  точка №{i} из {num_points}, x = {x:.15f}")
        print(f"  my_tan   = {mine:.15f}")
        print(f"  math.tan = {ref:.15f}")
        print(f"  |разность| = {abs_err:.3e}")
        print(f"  Всего точек с точным несовпадением: {mismatch_count} из {num_points}")
    else:
        print("\nТочных несовпадений с math.tan не найдено.")

    # Дополнительные диапазоны: большие аргументы (проверка редукции)
    print("\nБольшие аргументы (проверка редукции по периоду pi):")
    print(f"{'x':>14} {'my_tan':>22} {'math.tan':>22} {'|разность|':>14}")
    for x in (10.0, 100.0, 1000.0, 12345.678, -999.5, 1e6):
        mine = my_tan(x)
        ref = math.tan(x)
        print(f"{x:14.3f} {mine:22.15f} {ref:22.15f} {abs(mine-ref):14.3e}")

    # Скорость
    n = 20000
    t0 = time.perf_counter()
    for x in xs:
        for _ in range(n // num_points):
            my_tan(x)
    t1 = time.perf_counter()
    for x in xs:
        for _ in range(n // num_points):
            math.tan(x)
    t2 = time.perf_counter()
    print(f"\nСкорость ({n} вычислений): my_tan = {t1-t0:.3f} c, "
          f"math.tan = {t2-t1:.3f} c (C-реализация из libm ожидаемо быстрее)")


if __name__ == "__main__":
    test(100000)
