# -*- coding: utf-8 -*-
"""
Автоматические тесты для my_tan из tangens.py.

Запуск без pytest:
    python3 test_tangens.py

Запуск через pytest (если установлен):
    python3 -m pytest test_tangens.py -v

Идея каждого теста: сравниваем нашу функцию с эталоном.
Эталон - math.tan (в тестах его использовать МОЖНО, в самой my_tan - нельзя)
и известные точные значения: tan(0)=0, tan(pi/4)=1, tan(-x)=-tan(x) и т.д.
Числа с плавающей точкой нельзя сравнивать через ==, поэтому всегда
используем допуск (tolerance): math.isclose / абсолютную и относительную ошибку.
"""

import math

from дфи2 import my_tan, PI


def test_known_values():
    """Точные известные значения."""
    assert my_tan(0.0) == 0.0
    assert math.isclose(my_tan(PI / 4), 1.0, rel_tol=1e-14)
    assert math.isclose(my_tan(-PI / 4), -1.0, rel_tol=1e-14)
    assert math.isclose(my_tan(PI / 6), 1.0 / math.sqrt(3.0), rel_tol=1e-14)
    assert math.isclose(my_tan(PI / 3), math.sqrt(3.0), rel_tol=1e-14)


def test_axis_1000_points():
    """Главный тест по заданию: минимум 100 точек числовой оси.
    У нас 1000 точек на [-1.45, 1.45] (полюса +-pi/2 не включаем)."""
    num_points = 1000
    max_abs_err = 0.0
    max_rel_err = 0.0
    for i in range(num_points):
        x = -1.45 + 2.90 * i / (num_points - 1)
        mine = my_tan(x)
        ref = math.tan(x)
        abs_err = abs(mine - ref)
        rel_err = abs_err / abs(ref) if ref != 0 else abs_err
        max_abs_err = max(max_abs_err, abs_err)
        max_rel_err = max(max_rel_err, rel_err)
        # Комбинированный допуск: относительный + абсолютный (для x около 0,
        # где tan(x) ~ 0 и относительная ошибка не имеет смысла).
        assert abs_err <= 1e-12 * max(1.0, abs(ref)), f"x={x}: {mine} != {ref}"
    # Итоговая точность должна быть почти машинной (double: ~2.2e-16)
    assert max_rel_err < 1e-12, f"max_rel_err={max_rel_err}"
    print(f"  [axis] max_abs_err={max_abs_err:.3e}, max_rel_err={max_rel_err:.3e}")


def test_oddness_and_period():
    """Свойства функции: нечётность tan(-x)=-tan(x), период tan(x+pi)=tan(x)."""
    for x in (0.1, 0.5, 1.0, 1.4, 3.0, 10.0):
        assert math.isclose(my_tan(-x), -my_tan(x), rel_tol=1e-12, abs_tol=1e-15)
        assert math.isclose(my_tan(x + PI), my_tan(x), rel_tol=1e-9, abs_tol=1e-12)


def test_large_arguments():
    """Большие аргументы: проверка редукции по периоду.
    Допуск шире (1e-8): ошибка редукции x - k*pi растёт вместе с |x|."""
    for x in (10.0, 100.0, 1000.0, 12345.678, -999.5, 1e6):
        mine = my_tan(x)
        ref = math.tan(x)
        assert math.isclose(mine, ref, rel_tol=1e-8, abs_tol=1e-12), \
            f"x={x}: {mine} != {ref}"


def test_near_pole():
    """Около полюса pi/2: значение большое, знак правильный, точность сохранена."""
    x = PI / 2 - 1e-6
    mine = my_tan(x)
    ref = math.tan(x)
    assert mine > 1e5  # tan(pi/2 - 1e-6) ~ 1e6
    assert math.isclose(mine, ref, rel_tol=1e-9)
    # С другой стороны полюса знак меняется на минус
    assert my_tan(PI / 2 + 1e-6) < -1e5


def test_special_values():
    """Особые значения: NaN и бесконечности."""
    assert math.isnan(my_tan(float("nan")))
    assert math.isnan(my_tan(float("inf")))
    assert math.isnan(my_tan(float("-inf")))


if __name__ == "__main__":
    test_known_values()
    print("OK test_known_values")
    test_axis_1000_points()
    print("OK test_axis_1000_points")
    test_oddness_and_period()
    print("OK test_oddness_and_period")
    test_large_arguments()
    print("OK test_large_arguments")
    test_near_pole()
    print("OK test_near_pole")
    test_special_values()
    print("OK test_special_values")
    print("\nВсе тесты пройдены!")
