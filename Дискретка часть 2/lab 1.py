

#Task 2 =========================================================

n_complete = int(input('число вершин полного графа'))
n_tree = int(input("число вершин дерева"))

edges_complete = n_complete * (n_complete - 1) // 2
edges_tree = n_tree - 1

print("число ребер в полном графе",edges_complete)
print("число ребер в дереве",edges_tree)

#task 3 =========================================================

#
seq = list(map(int, input().split()))
n = len(seq)
d = sorted(seq, reverse=True)

if any(x < 0 for x in d):
    print("Невозможен")
    print("Есть отрицательная степень")
elif any(x > n - 1 for x in d):
    print("Невозможен")
    print("Степень больше n-1")
elif sum(d) % 2 == 1:
    print("Невозможен")
    print("Сумма степеней нечётная")
else:
    possible = True
    reason = ""
    for k in range(1, n):
        left = sum(d[:k])
        right = k * (k - 1) + sum(min(k, d[i]) for i in range(k, n))
        if left > right:
            possible = False
            reason = f"Нарушено неравенство Эрдёша-Галлаи при k={k}"
            break
    if possible:
        print("Возможен")
    else:
        print("Невозможен")
        print(reason)
#Task 4 ==========================================================

n_empty = int(input("Количество вершин пустого графа: "))
n_complete = int(input("Количество вершин полного графа: "))
n_tree = int(input("Количество вершин дерева: "))
n_cycle = int(input("Количество вершин простого цикла Cn: "))

chi_empty = 1
chi_complete = n_complete
chi_tree = 1 if n_tree <= 1 else 2
chi_cycle = 3 if n_cycle % 2 == 1 else 2

print("Хроматическое число пустого графа:", chi_empty)
print("Хроматическое число полного графа:", chi_complete)
print("Хроматическое число дерева:", chi_tree)
print("Хроматическое число простого цикла Cn:", chi_cycle)

#task 5


