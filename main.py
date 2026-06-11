import random
import time
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_mana = 100
        self.mana = 50
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = 0
        self.level = 1
        self._inventory = []

    @abstractmethod
    def attack_target(self, target):
        pass

    def take_damage(self, damage):
        dmg = max(1, damage - self.get_defense())
        self.hp -= dmg
        print(f'У {self.name} остаётся {self.hp} здоровья')
        return dmg

    def get_defense(self):
        return self.defense

    def get_attack_power(self):
        return self.attack

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, exp):
        self.exp += exp
        print(f'Персонаж {self.name} получает {exp} \n опыта и всего у него опыта {self.exp}')
        if self.exp >= self.level * 50:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.attack += 2
        self.max_hp += 2
        self.hp = self.max_hp
        self.defense += 2
        self.exp = 0
        self.creet_chans += 0.05

        print(
            f'Персонаж {self.name} повышает уровень до {self.level} \n и повышает характеристики : \n здоровье {self.hp},\n урон{self.attack},\n зашита{self.defense}')

    def show_inv(self):
        i = 0
        if not self._inventory:
            print('У вас нечего нет')
        else:
            for e in self._inventory:
                i += 1
                print(f"{i}.{e}")

    def add_item(self, item):
        self._inventory.append(item)
        print(f'Вы получили по заслугам ({item.name})!')

    def __str__(self):
        return f'Имя - {self.name} \n у него {self.hp}/{self.max_hp} здоровьья \n он бьёт с силой {self.attack} \n у него такая защита {self.defense} \n у него столко опыта {self.exp} и он на {self.level} левле'


class Item(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, character):
        pass

    def __str__(self):
        return f'{self.name} \n {self.description}'


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=6, attack=3, defense=3)
        self.rage = 0

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet = random.randint(1, 100)
        creet_chans = 13
        if creet <= creet_chans and self.rage == 50:
            now_dmg = dmg * 2 * 2
            self.rage = 0
        elif self.rage == 50:
            now_dmg = dmg * 2
            self.rage = 0
        elif creet <= creet_chans:
            now_dmg = dmg * 2
            self.rage += 1
        else:
            now_dmg = dmg
            self.rage += 1
        target.take_damage(now_dmg)
        return now_dmg


class Magician(Character):
    def __init__(self, name):
        super().__init__(name, hp=1, attack=5, defense=2)
        self.mana = 50
        self.max_mana = 100

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet_chans = 8
        creet = random.randint(1, 100)
        if creet <= creet_chans:
            now_dmg = dmg * 2
        else:
            now_dmg = dmg

        try:
            if self.mana >= 50:
                activation = input('Включить супер атаку(1) ')
                if activation == 1:
                    now_dmg = dmg * 3
                    self.mana -= 50
        except ValueError, TypeError:
            print('ты профукался')

        self.mana_regen()
        target.take_damage(now_dmg)
        return now_dmg

    def mana_regen(self):
        self.mana += 7
        if self.mana >= 50:
            print(f'У игрока{self.name} {self.mana} маны')

    # вызываем add_max_mana через проверку isinstance в функции битвы
    def add_max_mana(self):
        level = 0
        if self.level >= level:
            self.level = level
            self.max_mana += 25


class Archer(Character):
    def __init__(self, name):
        super().__init__(name, hp=9, attack=4, defense=3)
        self.accuracy = 10

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet_chans = 19
        creet = random.randint(1, 100)
        accuracy_func = random.randint(1, 100)
        add_dmg = 0
        if accuracy_func <= self.accuracy:
            add_dmg = dmg + dmg
        if creet <= creet_chans:
            now_dmg = dmg * 2 + add_dmg
        else:
            now_dmg = dmg
        target.take_damage(now_dmg)
        return now_dmg

    # вызываем add_accuracy через проверку isinstance в функции битвы
    def add_accuracy(self):
        level = 0
        if self.level >= level:
            self.level = level
            self.accuracy += 2


class HealingPotion(Item):
    def __init__(self, amount=4):
        super().__init__(f'Зелье здоровья (+{amount} hp)',
                         f'Редкая гадость:  острый перец и \n фарментированые (гнилые) помидоры \n (восстанавливает {amount} hp).')
        self.amount = amount

    def use(self, character):
        max_hp = character.max_hp
        character.hp += self.amount
        if character.hp > max_hp:
            character.hp = max_hp
        print(f"{character.name} востанавливает себе {self.amount} hp")
        return True


class ManaPotion(Item):
    def __init__(self, amount=4):
        super().__init__(f'Зелье маны (+{amount} hp)', f'Востанавливает {amount} маны')
        self.amount = amount

    def use(self, character):
        max_mana = character.max_mana
        character.mana += self.amount
        if character.mana > max_mana:
            character.mana = max_mana
            print(f"{character.name} востанавливает себе {self.amount} маны")
        return True


class Enemy(Character):
    def __init__(self, name, hp, attack, defense, exp):
        super().__init__(name, hp, attack, defense)
        self.exp = exp

    def attack_target(self, target):
        damage = self.get_attack_power()
        creet = random.randint(1, 100)
        if creet <= 8:
            damage *= 2
            print(f'{self.name} наносит крит удар по голове с тройным разворотом со спины')
        return target.take_damage(damage)


class AngryTeacher(Enemy):
    def __init__(self, name='Злой (м)учитель'):
        super().__init__(name, hp=3, attack=4, defense=3, exp=4)

    def attack_target(self, target):
        creet = random.randint(1, 100)
        first_time = 0
        damage = 0

        while first_time == 2:
            time.sleep(0.5)

            if creet <= 8:
                damage = self.get_attack_power()
                first_time += 1
                print(f'{self.name} наносит крит удар по голове с тройным разворотом со спины')
            else:
                damage = self.get_attack_power()
                damage /= 2
                print(f'{self.name} наносит удар')
        return target.take_damage(damage)


class EnemyOnBackOfTheClass(Enemy):
    def __init__(self, name='враг с задней парты'):
        super().__init__(name, hp=4, attack=4, defense=2, exp=6)
        self.chose = random.randint(1, 3)

    def attack_target(self, target):
        creet = random.randint(1, 100)
        # dodge = random.randint(1, 100)

        if creet <= 8:
            damage = self.get_attack_power()
            damage *= 2
            print(f'{self.name} наносит крит удар по голове с тройным разворотом со спины')
        else:
            damage = self.get_attack_power()
            print(f'{self.name} наносит удар')
        # if dodge <= 14 :
        # return target.take_damage ()
        return target.take_damage(damage)


class Game_Main:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_over = False
        self.count = 0

    def create_player(self):
        print('Создание персонажа из нечего \n (просто порох взорвался)')
        print()

        while True:
            try:
                chose_player = input('Введите \n 1 чтобы выбрать лучника, \n 2 чтоб мага и \n 3 чтоб воина ')
                print()
            except ValueError, TypeError:
                print('ты профукался')
            if chose_player == '1':
                name = input('Скажите ваше ИМЯ НЕМЕДЛЕНО ')
                print()
                self.player = Archer(name)
                print(f'ВЫ СОЗДАЛИ ЛУЧНИКА С ИМЕНЕМ {self.player.name}')
                print()
                break
            elif chose_player == '2':
                name = input('Скажите ваше ИМЯ НЕМЕДЛЕНО ')
                print()
                self.player = Magician(name)
                print(f'ВЫ СОЗДАЛИ МАГА С ИМЕНЕМ {self.player.name}')
                print()
                break
            elif chose_player == '3':
                name = input('Скажите ваше ИМЯ НЕМЕДЛЕНО ')
                print()
                self.player = Warrior(name)
                print(f'ВЫ СОЗДАЛИ ВОИНА С ИМЕНЕМ {self.player.name}')
                print()
                break
            else:
                print(f'Я СКАЗАЛ 1 или 2 или 3, а не {chose_player}!')
        print(self.player)

    def spawn_enemy(self):
        enemy = [EnemyOnBackOfTheClass, AngryTeacher]
        chose_enemy = random.choice(enemy)
        self.enemy = chose_enemy()
        print()
        print(f'На вас {self.enemy.name} напал  \n и у него {self.enemy}')

    def battle(self):
        self.count += 1
        print(f'Началась {self.count} битва')
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_player()
            if not self.enemy.is_alive():
                break
            self.turn_enemy()
        self.end_battle()

    def turn_player(self):
        while True:

            print('1 атака, \n 2 просмотр инветаря, \n 3 использовать предмет из инвентаря, \n 4 побег')
            player_chose = int(input('введите число '))
            if player_chose == 1:
                dmg = self.player.attack_target(self.enemy)
                print(f'Вы нанесли {dmg} урона!')
                print(f'У {self.enemy.name} осталось {self.enemy.hp} из {self.enemy.max_hp}')
                break
            elif player_chose == 2:
                self.player.show_inv()
                continue
            elif player_chose == 3:
                self.use_item()
                continue
            elif player_chose == 4:
                chans_esc = random.randint(1, 100)
                if chans_esc <= 39:
                    return True
                break
            elif player_chose == 2012:
                self.enemy.hp = 0
                continue
            else:
                print(f"Я СКАЗАЛ 1234, а не {player_chose}")
                break

    def turn_enemy(self):
        dmg = self.enemy.attack_target(self.player)
        print(f'{self.enemy.name} вам сносит {dmg} урона')

    def use_item(self):
        if not self.player._inventory:
            print('Вы бедьнее церковной мыши \n (у вас нечего нет)!')
            return
        print('Выбирите предмет для использованя')
        for i, item in enumerate(self.player._inventory, 1):
            print(f'{i}.{item}')
        player_chose = int(input('Выбирите предмет для использованья (числом) ')) - 1
        if 0 <= player_chose < len(self.player._inventory):
            item = self.player._inventory[player_chose]
            if item.use(self.player):
                self.player._inventory.pop(player_chose)
        else:
            print('Неправильно набран номер')

    def end_battle(self):
        self.count += 1
        if self.player.is_alive():
            print('Вы победители! \n вы чемпионы!')
            self.player.gain_exp(self.enemy.exp)
            if random.randint(1, 100) <= 65:
                loot = self.make_loot()
                self.player.add_item(loot)
        else:
            self.game_over = True

    def make_loot(self):
        item = [HealingPotion(5), HealingPotion(3), HealingPotion(6), HealingPotion(4), HealingPotion(2),
                HealingPotion(1)]
        if isinstance(self.player, Magician):
            item.append(ManaPotion(15))
            item.append(ManaPotion(18))
            item.append(ManaPotion(20))
            item.append(ManaPotion(30))
            item.append(ManaPotion(40))
            item.append(ManaPotion(49))
        return random.choice(item)

    def run(self):
        name = ['Саша', 'Владимир']
        print(f'Привет {random.choice(name)} я знаю это ты')
        self.create_player()
        while not self.game_over:
            self.spawn_enemy()
            self.battle()
            if not self.game_over:
                print(
                    f'Ваш могучий воин прошёл {self.count} битв, \n поднял уровень до {self.player.level} и \n получил {self.player.exp} опыта из {self.player.level * 50}!')
        else:
            print(f'Игра окончена!!!')


if __name__ == '__main__':
    game = Game_Main()
    game.run()