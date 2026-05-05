# возвращает таблицу истинности по кортежу значений функции 3 переменных
def truth_table_by_vec(v):
    assert(len(v) == 8)
    tt = {}
    i = 0
    for A in range(2):
        for B in range(2):
            for C in range(2):
                tt[A, B, C] = v[i]
                i += 1
    return tt

v_maj = (1, 1, 0, 0, 0, 1, 0, 1)
tt = truth_table_by_vec(v_maj)

# возвращает таблицу истинности по заданной функции 3 переменных
def truth_table_by_func(f):
    tt = {}
    for A in range(2):
        for B in range(2):
            for C in range(2):
                tt[A, B, C] = f(A, B, C)
    return tt

def f_maj(x, y, z):
    return x and y or x and z or y and z

def f(x, y, z):
    return y | z & ~x

#tt = truth_table_by_func(f_maj)
#tt = truth_table_by_func(f)
print(tt)

# СД "полином Жегалкина" -- это список списков из 3 элементов
#  такого вида: [1, 0, 1],
#  каждый элемент списка кодирует слагаемое,
#  где 0 - отсутствие переменной, 1 - наличие переменной

def xor_polynom_str(polynom):
    return '0' if polynom == [] else ' ⊕ '.join(map(term_str, polynom))


def term_str(term):
    assert(len(term) == 3)
    vars = ['x', 'y', 'z']
    s = []
    for i in range(3):
        if term[i] == 0:
            continue
        elif term[i] == -1:
            s.append('~' + vars[i])
        elif term[i] == 1:
            s.append(vars[i])
    if s == []:
        return '1'
    else:
        return '&'.join(s)

# тестирование
#term = [0, 0, 0]
#print(term_str(term))

# тестирование
#test_polynom = [[1, 0, 1], [1, 1, 0], [0, 0, 0]]
#print(xor_polynom_str(test_polynom))

def xor_polynom(tt):
    polynom = []
    triangle = []
    tt_line = []
    for A in range(2):
        for B in range(2):
            for C in range(2):
                tt_line.append(tt[A, B, C])
    for A in range(2):
        for B in range(2):
            for C in range(2):
                if A == 0 and B == 0 and C == 0:
                    triangle.append(tt_line)
                else:
                    new_tt_line = []
                    for i in range(len(tt_line) - 1):
                        new_tt_line.append(tt_line[i] ^ tt_line[i+1])   # XOR соседних
                    tt_line = new_tt_line
                    triangle.append(tt_line)
    # ... остальная часть без изменений

# возвращает СД "полином Жегалкина" по таблице истинности
def xor_polynom(tt):
    polynom = []
    triangle = []
    tt_line = []
    for A in range(2):
        for B in range(2):
            for C in range(2):
                tt_line.append(tt[A, B, C])
    for A in range(2):
        for B in range(2):
            for C in range(2):
                if A == 0 and B == 0 and C == 0:
                    triangle.append(tt_line)
                else:
                    new_tt_line = []
                    for i in range(len(tt_line) - 1):
                        new_tt_line.append(tt_line[i] ^ tt_line[i+1])   # XOR соседних
                    tt_line = new_tt_line
                    triangle.append(tt_line)
    for line in triangle:
        print(line)
    i = 0
    for A in range(2):
        for B in range(2):
            for C in range(2):
                if triangle[i][0] == 1:
                    polynom.append([A, B, C])
                i += 1
    return polynom

def calc_xor_monom(monom, A, B, C):
    val = True
    if monom[0]:
        val = val and A
    if monom[1]:
        val = val and B
    if monom[2]:
        val = val and C
    return val

def calc_xor_polynom(polynom, A, B, C):
    val = 0
    for monom in polynom:
        val ^= calc_xor_monom(monom, A, B, C)
    return val

def truth_table_of_xor_polynom(polynom):
    tt = {}
    for A in 0, 1:
        for B in 0, 1:
            for C in 0, 1:
                tt[A, B, C] = calc_xor_polynom(polynom, A, B, C)
    return tt

def print_truth_table(tt):
    for key in tt:
        print(key, tt[key])

polynom = xor_polynom(tt)
#print(polynom)
print(xor_polynom_str(polynom))

tt_polynom = truth_table_of_xor_polynom(polynom)
#print(tt_polynom)
print("Таблица истинности для функции")
print_truth_table(tt)

print("Таблица истинности для полинома Жегалкина")
print_truth_table(tt_polynom)