try:
    n = int(input("Введите количество пар чисел: "))
    count = 0

    for i in range(n):
        x, y = map(int, input(f"Введите пару {i + 1} (x y): ").split())
        if x < y:
            count += 1
    print(f"Количество пар, удовлетворяющих условию x < y: {count}")
except ValueError:
    print('не натуральное число или не пара')