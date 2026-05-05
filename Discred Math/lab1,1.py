# 1. Анекдоты
"""
В компании из n человек (n > 3) каждый узнал по одному новому
анекдоту (все анекдоты разные). За один телефонный разговор двое
сообщают друг другу все известные им анекдоты. Докажите, что за 2n − 4
звонков все смогут узнать все новые анекдоты.
"""

# 2. Печенья
"""
Печенюшки продаются пачками по 6 и по 13. Докажите, что вы всегда
можете купить некоторое количество пачек первого и второго типов так,
что в сумме вы получите заданное число, большее или равное 60.
"""

# 3. Монетки
"""
Даны n монет одинакового достоинства, среди которых имеется
одна фальшивая, отличающаяся весом. Доказать, что если n <= 3^k, то
достаточно k взвешиваний на чашечных весах, чтобы обнаружить
фальшивую монету.
"""

# Вход: количество человек n (n > 3)
# Выход: список пар (2-кортежей) номеров людей (от 1 до n):
#   кто с кем разговаривает,
#   звонков должно быть не более 2n-4
def sol_anecdotes(n):
    # место для вашего решения
    a=[(1, 2), (3, 4), (1, 3), (2, 4)]
    s=n-4
    if n == 4:
        return [(1, 2), (3, 4), (1, 3), (2, 4)]
    else:
        if n>4:
            while s>0:
                s=s-1
                a=[(1+s,s)]+a
            return a


# Тестирование решения задачи "Анекдоты" на заданном тесте
def test_anecdotes(n):
    ans = sol_anecdotes(n)  # вызов функции, решающей задачу
    # проверка количества звонков
    if len(ans) > 2 * n - 4:
        return False
    # инициализация: сначала каждый знает только свой анекдот
    # для каждого человека храним множество известных ему анекдотов
    familiar_anecdotes = []
    for i in range(n):
        familiar_anecdotes.append({i})
    # для каждого звонка обновляем множества известных анекдотов
    for call in ans:
        abonent1, abonent2 = call
        if not (abonent1 >= 1 and abonent1 <= n) or not (abonent2 >= 1 and abonent2 <= n):
            return False
        # приводим индексы к индексации с 0
        abonent1 -= 1
        abonent2 -= 1
        sum_anecdotes = familiar_anecdotes[abonent1].union(familiar_anecdotes[abonent2])
        familiar_anecdotes[abonent1] = sum_anecdotes
        familiar_anecdotes[abonent2] = sum_anecdotes
    ok = True
    for i in range(n):
        ok = ok and len(familiar_anecdotes[i]) == n
    return ok


# Вход: количество печеньев n (n >= 60)
# Выход: двухэлементный кортеж (a, b)
# a >= 0, b >= 0, 6a + 13b = n
# (a - количество пачек по 6 печеньев, b - количество пачек по 13 печеньев)
def sol_cookies(n):
    # место для вашего решения
    # (решением должен быть алгоритм, работающий на любом возможном тесте)
    if n == 60:
        return 10, 0
    elif n == 61:
        return 8, 1
    else:
        return 0, 0


# Тестирование решения задачи "Печенья" на заданном тесте
def test_cookies(n):
    a, b = sol_cookies(n)
    return a >= 0 and b >= 0 and 6 * a + 13 * b == n


# Вход: количество монет n (n >= 1)
# Программа должна за k взвешиваний на чашечных весах
#   (вызывая функцию weigh с указанием множеств номеров
#   взвешиваемых монет)
#   обнаружить фальшивую монету, где k <= ceil(log_3(n)),
#   ceil - округление вверх, log_3 - логарифм по основанию 3
# Выход: номер фальшивой монеты
def sol_coins(n):
    # место для вашего решения
    if n == 1:
        return 1
    elif n == 2:
        w = weigh({1}, {2})
        if w == 1:
            return 1
        else:
            return 2
    elif n == 3:
        w = weigh({1}, {2})
        if w == 1:
            return 1
        elif w == 2:
            return 2
        else:
            return 3
    else:
        return 1


# coins1, coins2 - два множества монет (индексы от 1 до n)
# выход: 1, если первая чашка перевешивает,
#   2, если вторая чашка перевешивает,
#   0, если чашки уравновешивают друг друга
def weigh(coins1, coins2):
    global num_weigh
    num_weigh += 1
    if len(coins1) > len(coins2):
        return 1
    elif len(coins1) < len(coins2):
        return 2
    else:
        global correct_ans
        if correct_ans in coins1:
            return 1
        elif correct_ans in coins2:
            return 2
        else:
            return 0


import random
import math
# Тестирование решения задачи "Монеты" на заданном тесте
def test_coins(n):
    global correct_ans
    correct_ans = random.choice(range(n)) + 1  # число от 1 до n
    global num_weigh
    num_weigh = 0
    ans = sol_coins(n)
    return ans == correct_ans and num_weigh <= math.ceil(math.log(n, 3))


def test_cases_anecdotes():
    test_cases = [4, 5, 6, 7, 10, 15, 20, 30, 59, 64, 72, 100]
    test_result = True
    print("Problem: Anecdotes")
    for i, test in enumerate(test_cases):
        print("Test", i + 1, "-- ", end='')
        res = test_anecdotes(test)
        test_result = test_result and res
        if res:
            print("Passed")
        else:
            print("Failed")
    print("Check result:")
    if test_result:
        print("  Accepted")
    else:
        print("  Rejected")
    print()


def test_cases_cookies():
    test_cases = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 83,
                  100, 153, 176, 188, 190, 191, 192, 193, 194, 195, 196, 197,
                  198, 199, 200, 201, 202, 203, 204, 205, 234, 300]
    test_result = True
    print("Problem: Cookies")
    for i, test in enumerate(test_cases):
        print("Test", i + 1, "-- ", end='')
        res = test_cookies(test)
        test_result = test_result and res
        if res:
            print("Passed")
        else:
            print("Failed")
    print("Check result:")
    if test_result:
        print("  Accepted")
    else:
        print("  Rejected")
    print()


def test_cases_coins():
    test_cases = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 21, 27, 28, 29, 30, 78, 79, 80, 81, 82, 83, 100]
    test_result = True
    print("Problem: Coins")
    for i, test in enumerate(test_cases):
        print("Test", i + 1, "-- ", end='')
        res = test_coins(test)
        test_result = test_result and res
        if res:
            print("Passed")
        else:
            print("Failed")
    print("Check result:")
    if test_result:
        print("  Accepted")
    else:
        print("  Rejected")
    print()


test_cases_anecdotes()
test_cases_cookies()
test_cases_coins()