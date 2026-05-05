import random
import json
import os


class Character:
    RACES = {
        # Бонусы применяются при создании персонажа.
        # dodge_bonus: добавка к шансу уклонения (0.10 = +10%)
        # potion_bonus: множитель лечения зельем (1.15 = +15%)
        "Человек": {"hp": 0, "atk": 0, "def": 0, "dodge_bonus": 0.00, "potion_bonus": 1.00},
        "Эльф": {"hp": -10, "atk": 2, "def": 0, "dodge_bonus": 0.15, "potion_bonus": 1.00},
        "Гном": {"hp": 15, "atk": 0, "def": 2, "dodge_bonus": -0.05, "potion_bonus": 1.05},
        "Орк": {"hp": 20, "atk": 4, "def": -1, "dodge_bonus": -0.10, "potion_bonus": 0.95},
        "Нежить": {"hp": 5, "atk": 1, "def": 1, "dodge_bonus": 0.00, "potion_bonus": 0.80},
    }

    def __init__(self, name, race="Человек"):
        self.name = name
        self.race = race if race in self.RACES else "Человек"
        self.level = 1
        self.exp = 0
        self.max_exp = 100

        base_health = random.randint(80, 120)
        base_attack = random.randint(10, 20)
        base_defense = random.randint(5, 15)
        race_bonus = self.RACES[self.race]

        self.max_health = max(1, base_health + race_bonus["hp"])
        self.health = self.max_health
        self.attack = max(1, base_attack + race_bonus["atk"])
        self.defense = max(0, base_defense + race_bonus["def"])
        self.dodge_bonus = race_bonus["dodge_bonus"]
        self.potion_bonus = race_bonus["potion_bonus"]
        self.inventory = {
            "health_potion": 2,
            "weapon": None,
            "armor": None
        }
        self.stat_points = 5

    def redistribute_stats(self):
        print(f"\nТекущие характеристики:")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")
        print(f"Доступные очки: {self.stat_points}")

        while self.stat_points > 0: 
            print("\nВыберите характеристику для улучшения:")
            print("1. Здоровье (+10 HP)")
            print("2. Атака (+2 ATK)")
            print("3. Защита (+1 DEF)")
            choice = input("Введите номер (или '0' для выхода): ")

            if choice == '0':
                break
            elif choice == '1':
                self.max_health += 10
                self.health = min(self.max_health, self.health + 10)
                self.stat_points -= 1
            elif choice == '2':
                self.attack += 2
                self.stat_points -= 1
            elif choice == '3':
                self.defense += 1
                self.stat_points -= 1
            else:
                print("Неверный ввод!")

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.max_exp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_exp = int(self.max_exp * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 3
        self.stat_points += 3
        print(f"\n🎉 Уровень повышен! Теперь вы {self.level} уровня!")
        print(f"Новые характеристики: HP={self.health}/{self.max_health}, ATK={self.attack}, DEF={self.defense}")

    def use_potion(self):
        if self.inventory["health_potion"] > 0:
            heal = random.randint(25, 40)
            heal = int(heal * self.potion_bonus)
            self.health = min(self.max_health, self.health + heal)
            self.inventory["health_potion"] -= 1
            print(f"Вы использовали зелье здоровья! Восстановлено {heal} HP.")
        else:
            print("У вас нет зелий здоровья!")

    def is_alive(self):
        return self.health > 0


class Enemy:
    TEMPLATES = {
        "Гоблин": {"hp": (45, 70), "atk": (7, 12), "def": (2, 7), "exp_mul": 1.0},
        "Волк": {"hp": (40, 65), "atk": (9, 14), "def": (1, 5), "exp_mul": 1.0},
        "Скелет": {"hp": (50, 80), "atk": (8, 13), "def": (3, 9), "exp_mul": 1.1},
        "Бандит": {"hp": (55, 85), "atk": (10, 16), "def": (2, 8), "exp_mul": 1.2},
        "Слизень": {"hp": (60, 95), "atk": (6, 11), "def": (4, 10), "exp_mul": 1.0},
        "Культист": {"hp": (55, 90), "atk": (11, 18), "def": (2, 7), "exp_mul": 1.3},
        "Огр": {"hp": (90, 140), "atk": (14, 22), "def": (3, 9), "exp_mul": 1.6},
        "Тролль": {"hp": (110, 170), "atk": (13, 21), "def": (5, 12), "exp_mul": 1.8},
        "Тёмный рыцарь": {"hp": (95, 150), "atk": (16, 25), "def": (7, 15), "exp_mul": 2.0},
        "Некромант": {"hp": (80, 130), "atk": (18, 27), "def": (4, 10), "exp_mul": 2.2},
        "Дракончик": {"hp": (120, 190), "atk": (20, 30), "def": (6, 14), "exp_mul": 2.5},
    }

    def __init__(self, name, level):
        self.name = name if name in self.TEMPLATES else random.choice(list(self.TEMPLATES.keys()))
        self.level = level
        tpl = self.TEMPLATES[self.name]
        lvl_scale = max(0.6, level / 2)
        self.health = random.randint(tpl["hp"][0], tpl["hp"][1]) * lvl_scale
        self.attack = random.randint(tpl["atk"][0], tpl["atk"][1]) * lvl_scale
        self.defense = random.randint(tpl["def"][0], tpl["def"][1]) * lvl_scale
        self.exp_mul = tpl["exp_mul"]

    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self):
        self.player = None
        self.locations = [
            "Темный лес",
            "Пещера гоблинов",
            "Заброшенный замок",
            "Магическая роща"
        ]
        self.current_location = 0

    def choose_race(self):
        races = list(Character.RACES.keys())
        print("\nВыберите расу:")
        for i, race in enumerate(races, start=1):
            b = Character.RACES[race]
            hp = f"{b['hp']:+d}"
            atk = f"{b['atk']:+d}"
            df = f"{b['def']:+d}"
            dodge = int(b["dodge_bonus"] * 100)
            pot = int((b["potion_bonus"] - 1.0) * 100)
            extra = []
            if dodge != 0:
                extra.append(f"уклонение {dodge:+d}%")
            if pot != 0:
                extra.append(f"лечение зельем {pot:+d}%")
            extra_str = f" ({', '.join(extra)})" if extra else ""
            print(f"{i}. {race}: HP {hp}, ATK {atk}, DEF {df}{extra_str}")
        choice = input("Введите номер (по умолчанию 1): ").strip()
        if not choice.isdigit():
            return races[0]
        idx = int(choice)
        if 1 <= idx <= len(races):
            return races[idx - 1]
        return races[0]

    def create_character(self):
        name = input("Введите имя вашего персонажа: ").strip()
        if not name:
            name = "Без имени"
        race = self.choose_race()
        self.player = Character(name, race=race)
        print(f"\nПривет, {self.player.name}! (Раса: {self.player.race})")
        self.player.redistribute_stats()

    def show_status(self):
        print(f"\n{'=' * 40}")
        print(f"Имя: {self.player.name}")
        print(f"Раса: {self.player.race}")
        print(f"Уровень: {self.player.level} (Опыт: {self.player.exp}/{int(self.player.max_exp)})")
        print(f"Здоровье: {self.player.health}/{self.player.max_health}")
        print(f"Атака: {self.player.attack}")
        print(f"Защита: {self.player.defense}")
        print(f"Зелья здоровья: {self.player.inventory['health_potion']}")
        print(f"Локация: {self.locations[self.current_location]}")
        print(f"{'=' * 40}")

    def battle(self, enemy):
        print(f"\n⚠️  Сражение с {enemy.name} (Уровень {enemy.level})!")
        print(f"{enemy.name}: HP={int(enemy.health)}, ATK={int(enemy.attack)}, DEF={int(enemy.defense)}")

        while self.player.is_alive() and enemy.is_alive():
            print("\nВаши действия:")
            print("1. Атаковать")
            print("2. Использовать зелье")
            print("3. Попытаться уклониться")

            choice = input("Выберите действие (1-3): ")

            if choice == '1':
                damage = max(1, self.player.attack - enemy.defense / 2)
                enemy.health -= damage
                print(f"Вы нанесли {damage:.1f} урона!")

                if enemy.is_alive():
                    enemy_damage = max(1, enemy.attack - self.player.defense / 2)
                    self.player.health -= enemy_damage
                    print(f"{enemy.name} нанес вам {enemy_damage:.1f} урона!")
                else:
                    print(f"Вы победили {enemy.name}!")
                    exp_gain = int(random.randint(30, 60) * enemy.level * getattr(enemy, "exp_mul", 1.0))
                    self.player.gain_exp(exp_gain)
                    print(f"Вы получили {exp_gain} опыта!")

            elif choice == '2':
                self.player.use_potion()
                if enemy.is_alive():
                    enemy_damage = max(1, enemy.attack - self.player.defense / 2)
                    self.player.health -= enemy_damage
                    print(f"{enemy.name} нанес вам {enemy_damage:.1f} урона!")

            elif choice == '3':
                dodge_chance = random.random()
                base_success = 0.60 + self.player.dodge_bonus
                base_success = max(0.05, min(0.95, base_success))
                if dodge_chance < base_success:
                    print("Вы успешно уклонились от атаки!")
                else:
                    enemy_damage = max(1, enemy.attack - self.player.defense / 2)
                    self.player.health -= enemy_damage
                    print(f"Уклонение не удалось! {enemy.name} нанес вам {enemy_damage:.1f} урона!")
            else:
                print("Неверный выбор!")

        if not self.player.is_alive():
            print("\n Вы погибли! Игра окончена.")
            return False
        return True

    def explore_location(self):
        event = random.choice(["enemy", "chest", "rest"])

        if event == "enemy":
            enemy_level = self.player.level + random.randint(-1, 2)
            enemy_level = max(1, enemy_level)
            loc = self.locations[self.current_location]
            if loc == "Темный лес":
                pool = ["Волк", "Гоблин", "Слизень", "Бандит"]
            elif loc == "Пещера гоблинов":
                pool = ["Гоблин", "Скелет", "Слизень", "Огр"]
            elif loc == "Заброшенный замок":
                pool = ["Скелет", "Бандит", "Тёмный рыцарь", "Некромант"]
            else:  # "Магическая роща"
                pool = ["Слизень", "Культист", "Тролль", "Дракончик"]

            if self.player.level >= 6 and random.random() < 0.15:
                pool = pool + ["Некромант", "Тёмный рыцарь", "Дракончик"]

            enemy = Enemy(random.choice(pool), enemy_level)
            return self.battle(enemy)

        elif event == "chest":
            item = random.choice(["health_potion", "weapon", "armor"])
            if item == "health_potion":
                amount = random.randint(1, 3)
                self.player.inventory["health_potion"] += amount
                print(f"\n Вы нашли {amount} зелья здоровья!")
            elif item == "weapon":
                if not self.player.inventory["weapon"]:
                    bonus = random.randint(5, 15)
                    self.player.attack += bonus
                    self.player.inventory["weapon"] = bonus
                    print(f"\n Вы нашли оружие! Ваша атака увеличена на {bonus}!")
            elif item == "armor":
                if not self.player.inventory["armor"]:
                    bonus = random.randint(3, 10)
                    self.player.defense += bonus
                    self.player.inventory["armor"] = bonus
                    print(f"\n Вы нашли броню! Ваша защита увеличена на {bonus}!")
            return True

        elif event == "rest":
            heal = random.randint(20, 40)
            self.player.health = min(self.player.max_health, self.player.health + heal)
            print(f"\n Вы нашли тихое место и отдохнули. Восстановлено {heal} HP.")
            return True

    def save_game(self):
        if self.player:
            data = {
                "name": self.player.name,
                "race": self.player.race,
                "level": self.player.level,
                "exp": self.player.exp,
                "max_exp": self.player.max_exp,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "attack": self.player.attack,
                "defense": self.player.defense,
                "inventory": self.player.inventory,
                "stat_points": self.player.stat_points,
                "current_location": self.current_location
            }
            with open("save_game.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Игра сохранена!")

    def load_game(self):
        if os.path.exists("save_game.json"):
            with open("save_game.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player = Character(data.get("name", "Без имени"), race=data.get("race", "Человек"))
            self.player.level = data["level"]
            self.player.exp = data["exp"]
            self.player.max_exp = data["max_exp"]
            self.player.max_health = data.get("max_health", data.get("health", self.player.max_health))
            self.player.health = data.get("health", self.player.max_health)
            self.player.attack = data["attack"]
            self.player.defense = data["defense"]
            self.player.inventory = data["inventory"]
            self.player.stat_points = data["stat_points"]
            self.current_location = data["current_location"]
            print("Игра загружена!")
            return True
        else:
            print("Сохранение не найдено!")
            return False

    def main_menu(self):
        while True:
            print("\n=== ГЛАВНОЕ МЕНЮ ===")
            print("1. Новая игра")
            print("2. Загрузить игру")
            print("3. Выйти")

            choice = input("Выберите вариант (1-3): ")

            if choice == '1':
                self.create_character()
                self.game_loop()
            elif choice == '2':
                if self.load_game():
                    self.game_loop()
            elif choice == '3':
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")

    def game_loop(self):
        while self.player and self.player.is_alive():
            self.show_status()

            print("\nДоступные действия:")
            print("1. Исследовать локацию")
            print("2. Перераспределить характеристики")
            print("3. Сохранить игру")
            print("4. Вернуться в главное меню")

            choice = input("Выберите действие (1-4): ")

            if choice == '1':
                if not self.explore_location():
                    break  # Игра окончена
            elif choice == '2':
                self.player.redistribute_stats()
            elif choice == '3':
                self.save_game()
            elif choice == '4':
                self.save_game()
                break
            else:
                print("Неверный выбор!")

            # Переход к следующей локации
            if random.random() < 0.3:  # 30% шанс перехода
                self.current_location = (self.current_location + 1) % len(self.locations)
                print(f"\n🌍 Вы перешли в новую локацию: {self.locations[self.current_location]}")


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.main_menu()