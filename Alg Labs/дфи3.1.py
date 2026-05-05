import sys


def info(name, var):
    print(f"\n{name}")
    print(f"Значение: {var}")
    print(f"Тип: {type(var)}")
    print(f"ID: {id(var)}")
    print(f"Размер (байт): {sys.getsizeof(var)}")


def odin():
    a = 100
    b = 100
    info("a", a)
    info("b", b)
    print(f"a is b: {a is b} ")


    list1 = [1, 2, 3]
    list2 = list1
    info("list1", list1)
    info("list2", list2)
    print(f"list1 is list2: {list1 is list2}")
    print(f"Изменяем list1: list1.append(4)")
    list1.append(4)
    print(f"list1: {list1}")
    print(f"list2: {list2}")
    print(f"list1 is list2: {list1 is list2}")

def raznita():
    x = 10
    y = x
    info("x (до изменения)", x)
    info("y (до изменения)", y)
    print(f"x is y: {x is y}")

    x = 20
    print("\nПосле x = 20:")
    info("x (после изменения)", x)
    info("y (после изменения)", y)
    print(f"x is y: {x is y}")

    list_a = [1, 2, 3]
    list_b = list_a
    info("list_a (до изменения)", list_a)
    info("list_b (до изменения)", list_b)
    print(f"list_a is list_b: {list_a is list_b}")

    list_a.append(4)
    print("\nПосле list_a.append(4):")
    info("list_a (после изменения)", list_a)
    info("list_b (после изменения)", list_b)
    print("list_b изменился, т.к. list_a и list_b указывают на один объект")

    list_c = list_a
    list_d = list_a.copy()
    info("list_c", list_c)
    info("list_d (копия через copy)", list_d)
    print(f"list_c is list_d: {list_c is list_d}")

    list_c.append(5)
    print("\nПосле list_c.append(5):")
    print(f"list_c: {list_c}")
    print(f"list_d: {list_d}")


def main():
    int = 42
    float = 3.14159
    str = "Hello, Python!"
    bool = True
    list = [1, 2, 3, 4, 5]
    tuple = (1, 2, 3)
    dict = {"item": "Абуз", "weight": 700}
    set = {1, 2, 3, 4, 5}

    variables = [
        ("int_var", int),
        ("float_var", float),
        ("str_var", str),
        ("bool_var", bool),
        ("list_var", list),
        ("tuple_var", tuple),
        ("dict_var", dict),
        ("set_var", set),
    ]

    for name, var in variables:
        info(name, var)
    odin()
    raznita()

main()