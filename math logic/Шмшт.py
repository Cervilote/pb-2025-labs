rivers = [
    {"name": "Амур", "length": 4416, "flow": 350, "basin": 1855, "source": "Яблоновый хребет", "mouth": "Татарский пролив"},
    {"name": "Лена", "length": 4400, "flow": 488, "basin": 2490, "source": "Байкальский хребет", "mouth": "Море Лаптевых"},
    {"name": "Обь", "length": 4100, "flow": 400, "basin": 2990, "source": "Предгорья Алтая", "mouth": "Карское море"},
    {"name": "Иртыш", "length": 4248, "flow": 323, "basin": 1643, "source": "Китай", "mouth": "Обь"},
    {"name": "Енисей", "length": 3487, "flow": 600, "basin": 2580, "source": "Восточный Саян", "mouth": "Карское море"},
    {"name": "Волга", "length": 3530, "flow": 255, "basin": 1360, "source": "Валдайская возвышенность", "mouth": "Каспийское море"},
    {"name": "Колыма", "length": 2129, "flow": 44, "basin": 643, "source": "Хребет Черского", "mouth": "Восточносибирское море"},
    {"name": "Урал", "length": 2428, "flow": 54, "basin": 231, "source": "Южный Урал", "mouth": "Каспийское море"},
    {"name": "Дон", "length": 2200, "flow": 45, "basin": 504, "source": "Среднерусская возвышенность", "mouth": "Азовское море"},
    {"name": "Кама", "length": 1805, "flow": 130, "basin": 507, "source": "Верхне-Камская возвышенность", "mouth": "Волга"},
    {"name": "Печора", "length": 1809, "flow": 130, "basin": 322, "source": "Северный Урал", "mouth": "Баренцево море"},
    {"name": "Ангара", "length": 1779, "flow": 62, "basin": 1039, "source": "Байкал", "mouth": "Енисей"},
    {"name": "Селенга", "length": 1024, "flow": 14, "basin": 447, "source": "Монголия", "mouth": "Байкал"},
    {"name": "Кубань", "length": 906, "flow": 11, "basin": 58, "source": "Кавказ", "mouth": "Азовское море"},
]
def get_river(name):
    for r in rivers:
        if r["name"] == name:
            return r
    raise ValueError("Река не найдена: " + name)
def P(x, y):
    return x["length"] >= y["length"]
def Q(x, y):
    return x["basin"] >= y["basin"]
def R(x):
    return "Байкал" in x["source"]
def R1(x):
    return x["mouth"] == "Азовское море"
kama = get_river("Кама")
lena = get_river("Лена")
pechora=get_river("Печора")
don=get_river("Дон")
ural=get_river("Урал")
result = []
result2 = []
result3= []
result4=[]
result5=[]
result6=[]
for x in rivers:
    if R1(x) or R(x):
        result2.append(x['name'])
for x in rivers:
    if P(x,pechora) and Q(don,x):
        result3.append(x['name'])
for x in rivers:
    if not(R1(x))and P(ural,x):
        result4.append(x['name'])

for x in rivers:
    if P(kama, x) or Q(x, lena):
        result.append(x["name"])
print("Результат выражения I (P(Кама, x) ∨ Q(x, Лена)):")
print('Всего соотвествий вырожения1:',len(result))
for name in result:
    print("*", name)        

print("\n1) R1(x) ∨ R(x)")
expr1 = [r["name"] for r in rivers if R1(r) or R(r)]
print(expr1)

print("\n2) P(x, Печора) ∧ Q(Дон, x)")
expr2 = [r["name"] for r in rivers if P(r, pechora) and Q(don, r)]
print(expr2)

print("\n3) R1(x) ∧ P(Урал, x)")
expr3 = [r["name"] for r in rivers if R1(r) and P(ural, r)]
print(expr3)

print("\n4) ∀x P(Амур, x) ∧ ∀y Q(x, Кубань)")
amur = get_river("Амур")
kuban = get_river("Кубань")
cond1 = all(P(amur, x) for x in rivers)
cond2_set = all(Q(y, kuban) for y in rivers)
print("--", cond1 and cond2_set)

print("\n5) ∃x ( R1(x) ∧ R(x) )")
expr5 = [r["name"] for r in rivers if R1(r) and R(r)]
exists = len(expr5) > 0
print("--", exists)

print('\n∃x P(Печора, x) V ∃y Q(Дон,x)')
cont=any(P(pechora,x)for x in rivers)
cont1=any(Q(don,x)for x in rivers)
print("--", cont or cont1)

print('\n∀x P(Печора, x)')
cont=all(P(pechora,x)for x in rivers)
print("--", cont)