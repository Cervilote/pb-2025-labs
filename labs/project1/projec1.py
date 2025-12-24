import random
import os
import json
from datetime import datetime


class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 5
        self.charisma = 3
        self.inventory = {"healing_potion": 3, "strength_potion": 1}
        self.specialization = ""
        self.location = "Опушка леса"

    def display_stats(self):
        print(f"\n=== ХАРАКТЕРИСТИКИ {self.name.upper()} ===")
        print(f"Уровень: {self.level}")
        print(f"Опыт: {self.exp}/{self.exp_to_level}")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")
        print(f"Харизма:{self.charisma}")
        print(f"Раса: {self.specialization}")
        print("Инвентарь:", self.inventory)

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        return amount

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 3

        print(f"\n🎉 Поздравляем! Вы достигли {self.level} уровня!")
        print("Ваши характеристики улучшены!")
        self.display_stats()

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            self.inventory[item] -= 1
            if item == "healing_potion":
                healed = self.heal(30)
                print(f"Использовано пирожок с вишней. Восстановлено {healed} здоровья.")
            if item == "strength_potion":
                self.attack += 5
                print("Использовано пирожок с манго. Атака увеличена на 5 на этот бой.")
            return True
        return False


class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward

    def display_stats(self):
        print(f"\n=== {self.name.upper()} ===")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Защита: {self.defense}")

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.health -= actual_damage
        return actual_damage


class Game:
    def __init__(self):
        self.player = None
        self.game_over = False
        self.locations = {
            "Опушка леса": {
                "description": "Вы находитесь на опушке леса. Вроде всё тихо.",
                "connections": ["Сумречный лес", "Заброщенный замок"],
                "events": ["rest", "find_item"]
            },
            "Сумречный лес": {
                "description": "Лес из в вечных сумраках. В воздухе витает странная энергия.",
                "connections": ["Опушка леса", "Вонючая пещера"],
                "events": ["enemy", "find_item"]
            },
            "Вонючая пещера": {
                "description": "Глубокая пещера, стены которой покрыты странной белой субстанцией.",
                "connections": ["Сумречный лес"],
                "events": ["boss", "treasure"]
            },
            "Заброщенный замок": {
                "description": "Заброшенный каменный замок. Кажется владелец за ним не очень хорошо следит.",
                "connections": ["Опушка леса", "Большая золотая комната"],
                "events": ["enemy", "find_item"]
            },
            "Большая золотая комната": {
                "description": "Огромная комната из золота. Здесь могут лежать всякие безделушки и не только.",
                "connections": ["Заброщенный замок"],
                "events": ["rest", "treasure"]
            }
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_character(self):
        self.clear_screen()
        print("=== СОЗДАНИЕ ПЕРСОНАЖА ===")
        name = input("Введите имя вашего персонажа: ")

        print("\nВыберите расу:")
        print("1. Высший эльф (высокий интеллект, бонус к исследованиям)")
        print("2. Дварф (улучшенная техника, бонус к ремонту)")
        print("3. Тифлинг (харизма, бонус к взаимодействию с командой)")
        print("4. Гоблин (Гнусавость, низкий рост, бесполезность, никчемность, -харизма)")

        while True:
            choice = input("> ")
            if choice in ["1", "2", "3", "4"]:
                break
            print("Пожалуйста, выберите 1, 2, 3 или 4")

        self.player = Character(name)

        if choice == "1":
            self.player.specialization = "Высший эльф"
            self.player.attack += 2
            self.player.inventory["research_tools"] = 1
        elif choice == "2":
            self.player.specialization = "Дварф"
            self.player.defense += 3
            self.player.inventory["tech_kit"] = 1
        elif choice == "3":
            self.player.specialization = "Тифлинг"
            self.player.defense += 3
            self.player.charisma += 4
            self.player.inventory["tech_kit"] = 1
        else:
            self.player.specialization = "Гоблин"
            self.player.max_health += 20
            self.player.health += 20
            self.player.charisma -=3

        print(f"\nОтлично! Вы - {self.player.specialization}")
        self.player.display_stats()

        input("\nНажмите Enter для продолжения...")

    def explore_location(self):
        location = self.locations[self.player.location]
        self.clear_screen()

        print(f"\n{location['description']}")
        print(f"\nДоступные направления: {', '.join(location['connections'])}")

        # Случайное событие
        event = random.choice(location['events'])

        if event == "enemy":
            self.encounter_enemy()
        elif event == "rest":
            self.rest_event()
        elif event == "find_item":
            self.find_item_event()
        elif event == "boss":
            self.boss_encounter()
        elif event == "treasure":
            self.treasure_event()

    def encounter_enemy(self):
        enemies = [
            Enemy("Маразматик", 40, 15, 1, 75),
            Enemy("6 7", 67, 2, 0, 67),
            Enemy("Камень", 70, 0, 10, 20),
            Enemy('Сын камня',50,0,7,15)
        ]

        enemy = random.choice(enemies)
        print(f"\n⚠️  Из тени появляется {enemy.name}!")

        self.combat(enemy)

    def boss_encounter(self):
        boss = Enemy("Титан Давид", 100, 15, 10, 200)
        print(f"\n💀 ПРЕДУПРЕЖДЕНИЕ: Обнаружен {boss.name}!")
        print("Это существо излучает невероятную мощь. Будьте осторожны!")

        self.combat(boss)

    def combat(self, enemy):
        print(f"\n=== БОЙ С {enemy.name.upper()} ===")

        while enemy.health > 0 and self.player.health > 0:
            print(f"\nВаше здоровье: {self.player.health} из {self.player.max_health}")
            print(f"Здоровье {enemy.name}: {enemy.health} из {enemy.max_health}")

            print("\nВыберите действие:")
            print("1. Атаковать")
            print("2. Использовать предмет")
            print("3. Попытаться уклониться")
            print("4. Пощадить")

            choice = input("> ")

            if choice == "1":
                # Атака игрока
                player_damage = max(1, self.player.attack + random.randint(-2, 3))
                damage_dealt = enemy.take_damage(player_damage)
                print(f"Вы нанесли {damage_dealt} урона существу '{enemy.name}'!")

            elif choice == "2":
                print("\nДоступные предметы:")
                items = list(self.player.inventory.keys())
                for i, item in enumerate(items, 1):
                    if self.player.inventory[item] > 0:
                        print(f"{i}. {item} ({self.player.inventory[item]} шт.)")

                try:
                    item_choice = int(input("Выберите предмет: ")) - 1
                    if 0 <= item_choice < len(items):
                        item_name = items[item_choice]
                        if self.player.use_item(item_name):
                            continue
                        else:
                            print("Не удалось использовать предмет!")
                            continue
                    else:
                        print("Неверный выбор!")
                        continue
                except ValueError:
                    print("Неверный ввод!")
                    continue

            elif choice == "3":
                dodge_chance = 30  # 30% шанс уклониться
                if random.randint(1, 100) <= dodge_chance:
                    print("Вы успешно уклонились от атаки!")
                    continue
                else:
                    print("Уклонение не удалось!")
            elif choice == "4":
                charm_chance = 10 + (self.player.charisma * 0.5)
                if random.randint(1,100) <= charm_chance:
                    print("Вы успешно заговорили зубы")
                    continue
                else:
                    print("Не особо разговорчивый оказался :(")
            else:
                print("Неверный выбор! Пропускаете ход.")

            # Атака врага (если ещё жив)
            if enemy.health > 0:
                enemy_damage = max(1, enemy.attack + random.randint(-2, 2))
                damage_taken = self.player.take_damage(enemy_damage)
                print(f"{enemy.name} атакует и наносит вам {damage_taken} урона!")

        if self.player.health <= 0:
            print(f"\n💀 {enemy.name} оттарабанил вас...")
            self.game_over = True
        else:
            print(f"\n🎉 Вы оттадрали {enemy.name}!")
            exp_gained = enemy.exp_reward
            self.player.add_exp(exp_gained)
            print(f"Получено экспухи: {exp_gained}")

            # Шанс найти предмет после боя
            if random.random() < 0.4:  # 40% шанс
                item = random.choice(["healing_potion", "strength_potion"])
                self.player.inventory[item] = self.player.inventory.get(item, 0) + 1
                print(f"Вы нашли {item}!")

    def rest_event(self):
        heal_amount = 25
        old_health = self.player.health
        self.player.heal(heal_amount)
        actual_heal = self.player.health - old_health

        print(f"\n✨ Вы нашли безопасное место полежать.")
        print(f"Восстановлено {actual_heal} здоровья.")
        print(f"Текущее здоровье: {self.player.health}/{self.player.max_health}")

        input("\nНажмите Enter для продолжения...")

    def find_item_event(self):
        items = {
            "healing_potion": "Зелье лечения",
            "strength_potion": "Зелье силы",
            "crystal_sample": "Образец кристалла"
        }

        item = random.choice(list(items.keys()))
        self.player.inventory[item] = self.player.inventory.get(item, 0) + 1

        print(f"\n🎁 Вы нашли {items[item]}!")
        print(f"Инвентарь: {self.player.inventory}")

        input("\nНажмите Enter для продолжения...")

    def treasure_event(self):
        print(f"\n💎 Вы нашли сокровищницу!")

        reward = random.choice([
            "large_heal",  # Полное лечение
            "exp_boost",  # Много опыта
            "stat_boost",  # Улучшение характеристик
            "rare_item"  # Редкий предмет
        ])

        if reward == "large_heal":
            old_health = self.player.health
            self.player.health = self.player.max_health
            print(f"Вы нашли медицинский комплекс! Здоровье полностью восстановлено!")

        elif reward == "exp_boost":
            exp_gain = 150
            self.player.add_exp(exp_gain)
            print(f"Вы нашли древние знания! Получено {exp_gain} опыта!")

        elif reward == "stat_boost":
            stat = random.choice(["attack", "defense"])
            if stat == "attack":
                self.player.attack += 3
                print("Вы поглотили красную энергию! Атака увеличена на 3!")
            else:
                self.player.defense += 3
                print("Вы поглотили синию энергию! Защита увеличена на 3!")

        elif reward == "rare_item":
            self.player.inventory["ancient_artifact"] = 1
            print("Вы нашли древний артефакт! Он может пригодиться позже...")

        input("\nНажмите Enter для продолжения...")

    def move_location(self):
        current_location = self.locations[self.player.location]

        print(f"\nКуда вы хотите отправиться?")
        connections = current_location['connections']

        for i, location in enumerate(connections, 1):
            print(f"{i}. {location}")

        while True:
            try:
                choice = int(input("> ")) - 1
                if 0 <= choice < len(connections):
                    self.player.location = connections[choice]
                    print(f"Вы перемещаетесь в {self.player.location}...")
                    break
                else:
                    print("Неверный выбор!")
            except ValueError:
                print("Пожалуйста, введите число")

        input("\nНажмите Enter для продолжения...")

    def save_game(self):
        save_data = {
            'player': {
                'name': self.player.name,
                'level': self.player.level,
                'exp': self.player.exp,
                'exp_to_level': self.player.exp_to_level,
                'health': self.player.health,
                'max_health': self.player.max_health,
                'attack': self.player.attack,
                'defense': self.player.defense,
                'inventory': self.player.inventory,
                'specialization': self.player.specialization,
                'location': self.player.location
            },
            'timestamp': datetime.now().isoformat()
        }

        filename = f"save_{self.player.name}.json"
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)

        print(f"Игра сохранена в файл {filename}")

    def load_game(self):
        print("Доступные сохранения:")
        saves = [f for f in os.listdir() if f.startswith('save_') and f.endswith('.json')]

        if not saves:
            print("Сохранения не найдены!")
            return False

        for i, save in enumerate(saves, 1):
            print(f"{i}. {save[5:-5]}")  # Убираем 'save_' и '.json'

        try:
            choice = int(input("Выберите сохранение: ")) - 1
            if 0 <= choice < len(saves):
                with open(saves[choice], 'r') as f:
                    save_data = json.load(f)

                self.player = Character(save_data['player']['name'])
                for key, value in save_data['player'].items():
                    if hasattr(self.player, key):
                        setattr(self.player, key, value)

                print(f"Игра загружена! Добро пожаловать, {self.player.name}!")
                return True
            else:
                print("Неверный выбор!")
                return False
        except (ValueError, FileNotFoundError, json.JSONDecodeError):
            print("Ошибка загрузки сохранения!")
            return False

    def main_menu(self):
        while not self.game_over:
            self.clear_screen()
            print("=== Игруха смехнявка ===")
            print("1. Продолжить игру")
            print("2. Посмотреть характеристики")
            print("3. Переместиться в другую локацию")
            print("4. Сохранить игру")
            print("5. Загрузить игру")
            print("6. Выйти из игры")

            choice = input("> ")

            if choice == "1":
                self.explore_location()
            elif choice == "2":
                self.player.display_stats()
                input("\nНажмите Enter для продолжения...")
            elif choice == "3":
                self.move_location()
            elif choice == "4":
                self.save_game()
                input("\nНажмите Enter для продолжения...")
            elif choice == "5":
                if self.load_game():
                    input("\nНажмите Enter для продолжения...")
            elif choice == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")

    def start(self):
        self.clear_screen()
        print("=== Игруха смехнявка ===")
        print("Вы проснулись посреди леса с болью в области чуть ниже поясницы.")
        print("Иди куда хотите и делайте, что сможете .\n")

        print("1. Новая игра")
        print("2. Загрузить игру")

        choice = input("> ")

        if choice == "1":
            self.create_character()
            self.main_menu()
        elif choice == "2":
            if self.load_game():
                input("\nНажмите Enter для продолжения...")
                self.main_menu()
            else:
                print("Создаем нового персонажа...")
                input("Нажмите Enter для продолжения...")
                self.create_character()
                self.main_menu()
        else:
            print("Неверный выбор, начинаем новую игру...")
            input("Нажмите Enter для продолжения...")
            self.create_character()
            self.main_menu()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start()