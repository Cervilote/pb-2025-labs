import math

# Словарь с функциями для всех вариантов
def get_function_by_name(name):
    """Возвращает функцию по её строковому представлению"""
    
    def create_function(expr):
        """Создает булеву функцию из выражения"""
        def func(x, y):
            # Заменяем логические операции на Python-эквиваленты
            # ¬x → y  (импликация: ¬x → y = x ∨ y)
            if expr == "¬x -> y":
                return (not x) <= y  # импликация: not x → y = (not x) <= y
            
            # x ∧ ¬y (конъюнкция)
            elif expr == "x ^ ¬y":
                return x and (not y)
            
            # ¬x ∨ y (дизъюнкция)
            elif expr == "¬x V y":
                return (not x) or y
            
            # ¬x ↔ ¬y (эквивалентность)
            elif expr == "¬x <-> ¬y":
                return (not x) == (not y)

            elif expr == "x <-> y":
                return (x) == (y)
            
            # ¬x ⊕ ¬y (сложение по модулю 2)
            elif expr == "¬x + ¬y":
                return (not x) ^ (not y)
            
            # ¬x ∧ ¬y (конъюнкция с отрицаниями)
            elif expr == "¬x ^ ¬y":
                return (not x) and (not y)
            
            # ¬x ⊥ ¬y (стрелка Пирса: NOT (x OR y))
            elif expr == "¬x | ¬y":
                return not ((not x) or (not y))
            
            # x → y (импликация)
            elif expr == "x -> y":
                return (not x) or y
            
            # x ∨ ¬y (дизъюнкция)
            elif expr == "x V ¬y":
                return x or (not y)
            
            # x ∨ y (дизъюнкция)
            elif expr == "x V y":
                return x or y
            
            # ¬x ⊕ y (сложение по модулю 2)
            elif expr == "¬x + y":
                return (not x) ^ y
            
            # x ⊕ y (сложение по модулю 2)
            elif expr == "x + y":
                return x ^ y
            
            else:
                raise ValueError(f"Неизвестная функция: {expr}")
        return func
    
    return create_function(name)

# Варианты систем функций
variants = [
    ["¬x -> y", "x ^ ¬y"],
    ["¬x V y", "¬x <-> ¬y"],
    ["¬x + ¬y", "¬x V y"],
    ["¬x ^ ¬y", "¬x -> y"],
    ["¬x | ¬y", "x -> y"],
    ["x V ¬y", "¬x -> y"],
    ["x V y", "¬x + y"],
    ["x -> y", "¬x ^ ¬y"],
    ["x <-> y", "¬x | ¬y"],
    ["x + y", "¬x V y"]
]

# Проверка принадлежности к классу T0 (сохраняющих 0)
def check_T0(f):
    return 1 if f(0, 0) == 0 else 0

# Проверка принадлежности к классу T1 (сохраняющих 1)
def check_T1(f):
    return 1 if f(1, 1) == 1 else 0

# Проверка принадлежности к классу L (линейных)
def check_L(f):
    f00 = f(0, 0)
    f01 = f(0, 1)
    f10 = f(1, 0)
    f11 = f(1, 1)
    
    # Вычисляем коэффициенты полинома Жегалкина
    a0 = f00
    a1 = f10 ^ a0
    a2 = f01 ^ a0
    a3 = f11 ^ a0 ^ a1 ^ a2
    
    return 1 if a3 == 0 else 0

# Проверка принадлежности к классу M (монотонных)
def check_M(f):
    # Проверяем все пары сравнимых наборов
    if f(0, 0) == 1 and f(0, 1) == 0:
        return 0
    if f(0, 0) == 1 and f(1, 0) == 0:
        return 0
    if f(0, 0) == 1 and f(1, 1) == 0:
        return 0
    if f(0, 1) == 1 and f(1, 1) == 0:
        return 0
    if f(1, 0) == 1 and f(1, 1) == 0:
        return 0
    return 1

# Проверка принадлежности к классу S (самодвойственных)
def check_S(f):
    if f(0, 0) == (1 ^ f(1, 1)):
        if f(0, 1) == (1 ^ f(1, 0)):
            return 1
    return 0

# Проверка полноты системы по критерию Поста
def check_completeness(functions, func_names):
    classes = ['T0', 'T1', 'L', 'M', 'S']
    results = []
    
    print("Анализ системы функций:")
    print("-" * 60)
    
    for i, (func, name) in enumerate(zip(functions, func_names), 1):
        t0 = check_T0(func)
        t1 = check_T1(func)
        l = check_L(func)
        m = check_M(func)
        s = check_S(func)
        
        results.append([t0, t1, l, m, s])
        print(f"Функция f{i}: {name:15} | T0={t0}, T1={t1}, L={l}, M={m}, S={s}")
    
    print("-" * 60)
    
    # Проверяем, есть ли в каждом классе функция, ему не принадлежащая
    completeness = True
    for j in range(5):
        class_has_non_member = False
        for i in range(len(functions)):
            if results[i][j] == 0:
                class_has_non_member = True
                break
        
        if not class_has_non_member:
            completeness = False
            print(f"Все функции принадлежат классу {classes[j]}")
        else:
            print(f"В классе {classes[j]} есть функция, ему не принадлежащая")
    
    return completeness

# Основная программа
if __name__ == "__main__":
    print("=" * 60)
    print("ПРОВЕРКА ПОЛНОТЫ СИСТЕМ БУЛЕВЫХ ФУНКЦИЙ")
    print("=" * 60)
    
    # Вывод всех вариантов
    print("\nДоступные варианты:")
    for i, variant in enumerate(variants, 1):
        print(f"{i}. {variant[0]} и {variant[1]}")
    
    # Ввод номера варианта
    while True:
        try:
            choice = int(input("\nВведите номер варианта (1-10): "))
            if 1 <= choice <= 10:
                break
            else:
                print("Ошибка: введите число от 1 до 10")
        except ValueError:
            print("Ошибка: введите целое число")
    
    # Получаем выбранный вариант
    selected_variant = variants[choice-1]
    func_names = selected_variant
    print(f"\nВыбран вариант {choice}: {func_names[0]} и {func_names[1]}")
    
    # Создаем функции для проверки
    functions = []
    for expr in selected_variant:
        functions.append(get_function_by_name(expr))
    
    print()
    
    # Проверяем полноту системы
    if check_completeness(functions, func_names):
        print("\nСИСТЕМА ФУНКЦИЙ ПОЛНА (по критерию Поста)")
    else:
        print("\nСИСТЕМА ФУНКЦИЙ НЕ ПОЛНА (по критерию Поста)")
    
    # Дополнительная информация - таблица истинности
    print("\n" + "=" * 60)
    print("ТАБЛИЦЫ ИСТИННОСТИ")
    print("=" * 60)
    
    for i, (func, name) in enumerate(zip(functions, func_names), 1):
        print(f"\nf{i}(x,y) = {name}")
        print("x y | f")
        print("----|---")
        for x in [0, 1]:
            for y in [0, 1]:
                print(f"{x} {y} | {int(func(x, y))}")