# Универсум - {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# структура данных "множество как двоичный вектор"
A_bin = [0, 1, 1, 0, 1, 0, 1, 0, 0, 1]

# структура данных "множество как список значений"
A = [1, 2, 4, 6, 9]

# преобразует множество из одного представления в другое -
#  двоичный вектор в список
def SET_convert_bin_to_list(M_bin):
    assert(len(M_bin) == 10)
    M_list = []
    for i in range(0, 10):
        if M_bin[i]:
            M_list.append(i)
    return M_list

# преобразует множество из одного представления в другое -
#  список в двоичный вектор
def SET_convert_list_to_bin(M_list):
    M_bin = [0] * 10
    for elem in M_list:
        M_bin[elem] = 1
    return M_bin

# возвращает объединение двух множеств, представленных
#  в виде двоичных векторов
def SET_bin_union(A, B):
    result = []
    for i in range(10):
        # Элемент входит в объединение, если он есть хотя бы в одном множестве
        result.append(1 if A[i] or B[i] else 0)
    return result

# возвращает пересечение двух множеств, представленных
#  в виде двоичных векторов
def SET_bin_intersection(A, B):
    result = []
    for i in range(10):
        # Элемент входит в пересечение, если он есть в обоих множествах
        result.append(1 if A[i] and B[i] else 0)
    return result

# возвращает разность двух множеств, представленных
#  в виде двоичных векторов (A \ B)
def SET_bin_difference(A, B):
    result = []
    for i in range(10):
        # Элемент входит в разность, если он есть в A, но отсутствует в B
        result.append(1 if A[i] and not B[i] else 0)
    return result

# возвращает симметрическую разность двух множеств, представленных
#  в виде двоичных векторов (элементы, входящие только в одно из множеств)
def SET_bin_symm_difference(A, B):
    result = []
    for i in range(10):
        # Элемент входит в симметрическая разность, если он есть ровно в одном множестве
        result.append(1 if A[i] != B[i] else 0)
    return result

# возвращает дополнение множества A (элементы универсума, не входящие в A)
def SET_bin_complement(A):
    result = []
    for i in range(10):
        # Дополнение: инвертируем каждый бит
        result.append(0 if A[i] else 1)
    return result

def test_set_operations(A_list, B_list):
    A_bin = SET_convert_list_to_bin(A_list)
    B_bin = SET_convert_list_to_bin(B_list)
    print("Множества:", SET_convert_bin_to_list(A_bin), SET_convert_bin_to_list(B_bin))
    print("Объединение:", SET_convert_bin_to_list(SET_bin_union(A_bin, B_bin)))
    print("Пересечение:", SET_convert_bin_to_list(SET_bin_intersection(A_bin, B_bin)))
    print("Разность (A \ B):", SET_convert_bin_to_list(SET_bin_difference(A_bin, B_bin)))
    print("Симметрическая разность:", SET_convert_bin_to_list(SET_bin_symm_difference(A_bin, B_bin)))
    print("Дополнение A:", SET_convert_bin_to_list(SET_bin_complement(A_bin)))

print(SET_convert_bin_to_list(A_bin))
print(SET_convert_list_to_bin(A))

# тестирование
A = [4, 5, 3, 1, 9]
B = [1, 2, 3, 4, 5]
test_set_operations(A, B)


M = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0]  # математика
I = [0, 1, 0, 1, 1, 0, 0, 0, 0, 1]  # информатика
P = [0, 0, 1, 0, 1, 0, 1, 1, 0, 0]  # физика
N = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1]  # новые
O = [1, 0, 1, 0, 1, 0, 0, 1, 1, 0]  # старые


math_or_physics = SET_bin_union(M, P)
guy_books = SET_bin_intersection(O, math_or_physics)
guy_list = SET_convert_bin_to_list(guy_books)


girl_books = SET_bin_intersection(N, I)
girl_list = SET_convert_bin_to_list(girl_books)

print("Возможности для парня:", guy_list)
print("Возможности для девушки:", girl_list)

# Все возможные пары
print("\nВсе возможные комбинации:")
for guy_book in guy_list:
    for girl_book in girl_list:
        if guy_book != girl_book:  # книги должны быть разными
            print(f"({guy_book}, {girl_book})")

# Пример выбора книг для чтения
S = SET_convert_list_to_bin([1, 2, 3, 5, 7])  # книги на полке
R = SET_convert_list_to_bin([2, 5])  # уже читает
to_read = SET_bin_difference(S, R)
to_read_list = SET_convert_bin_to_list(to_read)
print(f"\nКниги для чтения: {to_read_list}")

