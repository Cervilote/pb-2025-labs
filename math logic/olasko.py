

def count_colors(x, y, r):
    # Упрощение: переносим центр в первую четверть
    x = abs(x)
    y = abs(y)

    P0 = (y <= r) or (x <= r)
    

    P1 = True
    
 
    P2 = x < r
    

    P3 = (x**2 + y**2) <= r**2

    P4 = y < r
    

    predicates = [P0, P1, P2, P3, P4]
    count = sum(predicates)
    
    return count


# Примеры использования
if __name__ == "__main__":
    # Тестовые случаи
    test_cases = [
        (0, 0, 5),      # Круг с центром в начале координат
        (3, 4, 5),      # Круг в первой четверти
        (10, 10, 5),    # Круг полностью в первой четверти
        (2, 2, 10),     # Большой круг
    ]
    
    #print("Тестирование функции count_colors:")
    #for x, y, r in test_cases:
    #    colors = count_colors(x, y, r)
    #    print(f"Круг с центром ({x}, {y}) и радиусом {r}: {colors} различных цветов")
    
    # Интерактивный ввод
    print("\nВведите данные круга:")
    try:
        x = float(input("x = "))
        y = float(input("y = "))
        r = float(input("r = "))
        result = count_colors(x, y, r)
        print(f"\nКруг содержит {result} различных цветов")
    except ValueError:
        print("Ошибка ввода. Используйте числа.")

