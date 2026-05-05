import time
import random
import sys

sys.setrecursionlimit(200000)  # Для рекурсии на большом массиве


def generate_array(n):
    return [random.randint(1, 1000000) for _ in range(n)]


def find_max_brute_force(arr):
    n = len(arr)
    for i in range(n):
        is_max = True
        for j in range(n):
            if arr[j] > arr[i]:
                is_max = False
                break
        if is_max:
            return arr[i]
    return None


# 2. GREEDY - O(n)
def find_max_greedy(arr):
    if not arr:
        return None
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val


def find_max_divide_conquer(arr, left, right):
    if left == right:
        return arr[left]

    mid = (left + right) // 2
    left_max = find_max_divide_conquer(arr, left, mid)
    right_max = find_max_divide_conquer(arr, mid + 1, right)

    return max(left_max, right_max)


def find_max_dp(arr):
    if not arr:
        return None

    dp = [0] * len(arr)
    dp[0] = arr[0]

    for i in range(1, len(arr)):
        dp[i] = max(dp[i - 1], arr[i])

    return dp[-1]


def measure_time(func, arr, *args):
    start = time.time()
    if args:
        result = func(arr, *args)
    else:
        result = func(arr)
    end = time.time()
    return result, end - start


def main():
    n = 100000
    arr = generate_array(n)
    results = []
    # 1. Brute Force
    print("\n1. BRUTE FORCE")
    print("   Сложность: O(n²)")
    print("   сравниваем каждый элемент с каждым")
    try:
        result, duration = measure_time(find_max_brute_force, arr)
        print(f"   Результат: {result}")
        print(f"   Время: {duration:.6f} сек")
        print("   ⚠️  Для полного массива время оценивается в ~часы")
    except Exception as e:
        print(f"   Ошибка: {e}")

    # 2. Greedy
    print("\n2. GREEDY (Жадный алгоритм)")
    print("   Сложность: O(n)")
    print("   Идея: один проход, обновляем текущий максимум")
    result, duration = measure_time(find_max_greedy, arr)
    print(f"   Результат: {result}")
    print(f"   Время: {duration:.6f} сек")

    # 3. Divide & Conquer
    print("\n3. DIVIDE & CONQUER (Разделяй и властвуй)")
    print("   Сложность: O(n log n)")
    print("   Идея: рекурсивно делим массив пополам и находим максимум")
    result, duration = measure_time(find_max_divide_conquer, arr, 0, len(arr) - 1)
    print(f"   Результат: {result}")
    print(f"   Время: {duration:.6f} сек")

    # 4. DP
    print("\n4. DYNAMIC PROGRAMMING (Динамическое программирование)")
    print("   Сложность: O(n)")
    print("   Идея: dp[i] = max(dp[i-1], arr[i])")
    result, duration = measure_time(find_max_dp, arr)
    print(f"   Результат: {result}")
    print(f"   Время: {duration:.6f} сек")

    # Сравнительная таблица
    print("\n" + "=" * 70)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ")
    print("=" * 70)
    print(f"{'Алгоритм':<25} {'Сложность':<15} {'Время (сек)':<15} {'Оценка'}")
    print("-" * 70)
    print(f"{'Brute Force':<25} {'O(n²)':<15} {'~часы':<15} ")

    _, greedy_time = measure_time(find_max_greedy, arr)
    _, dc_time = measure_time(find_max_divide_conquer, arr, 0, len(arr) - 1)
    _, dp_time = measure_time(find_max_dp, arr)

    print(f"{'Greedy':<25} {'O(n)':<15} {greedy_time:<15.6f} ")
    print(f"{'Divide & Conquer':<25} {'O(n log n)':<15} {dc_time:<15.6f} ")
    print(f"{'DP (Tabulation)':<25} {'O(n)':<15} {dp_time:<15.6f} ")

    # Выводы
    print("\n" + "=" * 70)
    print("ВЫВОДЫ")
    print("=" * 70)
    print("""
1. BRUTE FORCE (O(n²)):
   - Самый медленный, для n=100000 практически не применим
   - Сравнивает каждый элемент с каждым, делая n² операций
   - Используется только для очень маленьких массивов

2. GREEDY (O(n)):
   - Самый эффективный для данной задачи
   - Требует всего один проход по массиву
   - Минимальное использование памяти
   - Рекомендуемый подход для поиска максимума

3. DIVIDE & CONQUER (O(n log n)):
   - Рекурсивный подход, элегантный для понимания
   - Медленнее линейных алгоритмов из-за рекурсивных вызовов
   - Хорош для параллельных вычислений на больших данных

4. DYNAMIC PROGRAMMING (O(n)):
   - Линейная сложность, как и Greedy
   - Использует дополнительную память O(n) для таблицы dp
   - Избыточен для простого поиска максимума

  ЛУЧШИЙ ПОДХОД: Greedy
   - Простота реализации
   - Оптимальная сложность O(n)
   - Минимальные затраты памяти O(1)
    """)



main()