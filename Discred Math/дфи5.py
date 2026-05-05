def analyze_relation(R):
    """
    Выясняет свойства отношения, заданного квадратной булевой матрицей R
    """
    n = len(R)

    # Рефлексивность: все элементы на главной диагонали равны 1
    reflexive = all(R[i][i] == 1 for i in range(n))

    # Симметричность: для всех i, j: R[i][j] == R[j][i]
    symmetric = all(R[i][j] == R[j][i] for i in range(n) for j in range(n))

    # Транзитивность: если R[i][j] == 1 и R[j][k] == 1, то R[i][k] == 1
    transitive = True
    for i in range(n):
        for j in range(n):
            if R[i][j] == 1:
                for k in range(n):
                    if R[j][k] == 1 and R[i][k] != 1:
                        transitive = False
                        break
            if not transitive:
                break
        if not transitive:
            break

    print("Рефлексивность:", reflexive)
    print("Симметричность:", symmetric)
    print("Транзитивность:", transitive)


def transitive_closure(R):
    n = len(R)
    closure = [row[:] for row in R]

    for k in range(n):
        for i in range(n):
            if closure[i][k] == 1:
                for j in range(n):
                    if closure[k][j] == 1:
                        closure[i][j] = 1
    return closure

#def inv(R):
#    n=len(R)
#   R_inv = [[R[j][i] for j in range(n)] for i in range(n)]
#    return R_inv

def print_relation(R):
    for row in R:
        print(list(map(int, row)))


A1 = ["Иванов", "Петров", "Сидоров", "Петечкин", "Васечкин"]
n1 = len(A1)

R1 = [[0 for _ in range(n1)] for _ in range(n1)]
R1_list = [("Иванов", "Петров"), ("Петров", "Сидоров"), ("Иванов", "Петечкин")]

for p in R1_list:
    ind1 = A1.index(p[0])
    ind2 = A1.index(p[1])
    R1[ind1][ind2] = 1

print_relation(R1)  # используем определение из нижней части
analyze_relation(R1)



A2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
n2 = len(A2)


def F2(x, y):
    return (x < y)


R2 = [[F2(A2[i], A2[j]) for j in range(n2)] for i in range(n2)]
print_relation(R2)
analyze_relation(R2)

print("\nТранзитивное замыкание:")
R2_closure = transitive_closure(R2)
print_relation(R2_closure)
analyze_relation(R2_closure)


A3 = A2
n3 = len(A3)


def F3(x, y):
    return (x + y) % 2 == 0


R3 = [[F3(A3[i], A3[j]) for j in range(n3)] for i in range(n3)]
print_relation(R3)
analyze_relation(R3)
#print(inv(R3))

print("\nТранзитивное замыкание:")
R3_closure = transitive_closure(R3)
print_relation(R3_closure)
analyze_relation(R3_closure)
