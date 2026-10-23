class Balance:
    def __init__(self, rub=0, kop=0):
        self.balance = rub * 100 + kop

    def __str__(self):
        rub = self.balance // 100
        kop = self.balance % 100
        return f"Balance = {rub:2} rub {kop:02} kop"

    def deposit(self, rub, kop=0):
        self.balance += rub * 100 + kop

    def withdraw(self, rub, kop=0):
        self.balance -= rub * 100 + kop


b1 = Balance(100)

for i in range(1000):
    b1.withdraw(0, 10)
    print(b1)