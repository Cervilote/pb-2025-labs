print("Введите 5 натуральных чисел:")
chisla = []
try:
    for i in range(5):

            num = int(input(f"Число {i+1}: "))
            if num>=0:
                chisla.append(num)
            else:
                print('не натуральное число')

except ValueError:
    print('не натуральное число')
try:
    pari = []
    for i in range(5):
        for j in range(5):
            if i != j:
                x = chisla[i]
                y = chisla[j]
                if x < y:
                    pari.append((x, y))
    if pari:
        pari=list(set(pari))
        output = " ".join([f"({pair[0]}, {pair[1]})" for pair in pari])
        print("Пары, удовлетворяющие условию x < y:")
        print(output)
    else:
        print("Нет пар, удовлетворяющих условию x < y.")
except IndexError:
    print("не натуральное число")