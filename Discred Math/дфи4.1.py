# Операции над множествами в виде упорядоченных списков

def SET_list_union(A, B):
    """Объединение двух упорядоченных множеств"""
    result = []
    i, j = 0, 0
    len_A, len_B = len(A), len(B)

    while i < len_A and j < len_B:
        if A[i] < B[j]:
            result.append(A[i])
            i += 1
        elif A[i] > B[j]:
            result.append(B[j])
            j += 1
        else:  # A[i] == B[j]
            result.append(A[i])  # Добавляем один раз
            i += 1
            j += 1

    # Добавляем оставшиеся элементы
    result.extend(A[i:])
    result.extend(B[j:])
    return result

def SET_list_intersection(A, B):
    """Пересечение двух упорядоченных множеств"""
    result = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            i += 1
        elif A[i] > B[j]:
            j += 1
        else:  # A[i] == B[j] — общий элемент
            result.append(A[i])
            i += 1
            j += 1
    return result

def SET_list_difference(A, B):
    """Разность множеств A \ B (элементы A, которых нет в B)"""
    result = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            result.append(A[i])
            i += 1
        elif A[i] > B[j]:
            j += 1
        else:  # A[i] == B[j] — элемент есть в B, пропускаем
            i += 1

    # Добавляем оставшиеся элементы A (они гарантированно больше всех в B)
    result.extend(A[i:])
    return result

def SET_list_symm_difference(A, B):
    """Симметрическая разность (элементы, входящие только в одно из множеств)"""
    result = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            result.append(A[i])
            i += 1
        elif A[i] > B[j]:
            result.append(B[j])
            j += 1
        else:  # A[i] == B[j] — элемент в обоих, пропускаем
            i += 1
            j += 1

    # Добавляем оставшиеся элементы из обоих списков
    result.extend(A[i:])
    result.extend(B[j:])
    return result

def SET_list_complement(A, universe=None):
    """Дополнение множества A до универсума"""
    if universe is None:
        universe = list(range(10))  # {0,1,2,...,9}

    result = []
    j = 0  # индекс в множестве A

    for elem in universe:
        # Если текущий элемент универсума есть в A, пропускаем его
        if j < len(A) and A[j] == elem:
            j += 1
        else:
            result.append(elem)
    return result

def test_ordered_set_operations(A_list, B_list):
    """Тестирование операций над упорядоченными множествами"""
    # Сортируем входные списки и удаляем дубликаты
    A = sorted(set(A_list))
    B = sorted(set(B_list))

    print("Множества:", A, B)
    print("Объединение:", SET_list_union(A, B))
    print("Пересечение:", SET_list_intersection(A, B))
    print("Разность (A \ B):", SET_list_difference(A, B))
    print("Симметрическая разность:", SET_list_symm_difference(A, B))
    print("Дополнение A:", SET_list_complement(A))
    print()

# Тестирование
print("ТЕСТИРОВАНИЕ УПОРЯДОЧЕННЫХ МНОЖЕСТВ")
print("=" * 40)

A = [4, 5, 3, 1, 9, 1]  # с дубликатом
B = [1, 2, 3, 4, 5]
test_ordered_set_operations(A, B)

# Дополнительные тесты
A2 = [1, 3, 5, 7]
B2 = [2, 4, 6, 8]
print("Дополнительный тест:")
test_ordered_set_operations(A2, B2)
