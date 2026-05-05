def composition_of_relations(R1, R2):
    """
    Параметры:
    R1 - булева матрица отношения R1 на множествах A и B
    R2 - булева матрица отношения R2 на множествах B и C
    Результат:
    R3 - булева матрица суперпозиции отношений R1 и R2 на множествах A и C
    """
    n1 = len(R1)
    m1 = len(R1[0])
    n2 = len(R2)
    m2 = len(R2[0])
    assert(m1 == n2)

    n3 = n1
    m3 = m2

    R3 = [[0 for _ in range(m3)] for _ in range(n3)]

    # Вычисляем R3 = R1 ◦ R2
    for i in range(n3):
        for k in range(m3):
            # Проверяем, существует ли j такое, что R1[i][j] == 1 и R2[j][k] == 1
            for j in range(m1):
                if R1[i][j] == 1 and R2[j][k] == 1:
                    R3[i][k] = 1
                    break
    return R3



def convert_relation_to_bin(R_list, A, B):
    """
    Преобразует отношение из списка пар в булеву матрицу
    """
    n = len(A)
    m = len(B)
    R = [[0 for _ in range(m)] for _ in range(n)]
    for pair in R_list:
        ind1 = A.index(pair[0])
        ind2 = B.index(pair[1])
        R[ind1][ind2] = 1
    return R


def print_relation(R):
    for row in R:
        print(list(map(int, row)))


# студенты
A = ["Иванов", "Петров", "Сидоров", "Петечкин", "Васечкин"]
n = len(A)

# преподаватели
B = ["Голодная", "Солодухин", "Рогулин"]
m = len(B)

# аудитории
C = [1443, 1444, 1447, 1503]
k = len(C)

# отношение СтудентПреподаватель - кого ищет студент
R1_list = [("Иванов", "Солодухин"), ("Петечкин", "Рогулин"), ("Сидоров", "Рогулин"), ("Васечкин", "Голодная")]
# отношение ПреподавательАудитория - в каких аудиториях может находиться преподаватель
R2_list = [("Голодная", 1443), ("Солодухин", 1443), ("Солодухин", 1447), ("Рогулин", 1503)]

# находим булевы матрицы отношений
R1 = convert_relation_to_bin(R1_list, A, B)
R2 = convert_relation_to_bin(R2_list, B, C)
# отношение СтудентАудитории - какие аудитории следует посетить
R3 = composition_of_relations(R1, R2)

print("A =", A)
print("B =", B)
print("C =", C)
print("R1")
print_relation(R1)
print("R2")
print_relation(R2)
print("R3")
print_relation(R3)

for i in range(n):
    for j in range(k):
        if R3[i][j]:
            print('(', A[i], ', ', C[j], ')', end='; ', sep='')