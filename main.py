import random
import time
from abc import ABC, abstractmethod
from os import name


class Character(ABC):
    def __init__(self, name, hp, attack, defense, exp, level, creet_chans, mana, max_mana):
        self.name = name
        self.max_mana = mana
        self.mana = mana
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.level = level
        self._inventory = []
        self.creet_chans = creet_chans

    @abstractmethod
    def attack_target(self, target):
        pass

    def take_damage(self, damage):
        dmg = max(1, damage - self.get_defense())
        self.hp -= dmg
        print(f'персонаж {self.name} получает {dmg} урона и у него остаётся {self.hp} здоровья')
        return dmg

    def get_defense(self):
        return self.defense

    def get_attack_power(self):
        return self.attack

    def is_alive(self):
        return self.hp > 0

    def gain_exp(self, exp):
        self.exp += exp
        print(f'персонаж {self.name} получает {exp} опыта и всего у него опыта {self.exp}')
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
            f'персонаж {self.name} повышает уровень до {self.level} и повышает характеристики : здоровье {self.hp},урон{self.attack},зашита{self.defense}')

    def show_inv(self):
        i = 0
        if not self._inventory:
            print('у вас нечего нет')
        else:
            for e in self._inventory:
                i += 1
                print(f"{i}.{e}")

    def __str__(self):
        return f'твоё имя - {self.name} у вас {self.hp}/{self.max_hp} здоровьья вы бьёте с силой {self.attack} у вас такая защита {self.defense} у вас столко опыта {self.exp}и вы на {self.level} левле'


class Item(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, character):
        pass

    def __str__(self):
        return f'{self.name} {self.description}'


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=6, attack=3, defense=3, creet_chans=13)
        self.rage = 0

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet = random.randint(1, 100)
        if creet <= self.creet_chans and self.rage == 50:
            now_dmg = dmg * 2 * 2
            self.rage = 0
        elif self.rage == 50:
            now_dmg = dmg * 2
            self.rage = 0
        elif creet <= self.creet_chans:
            now_dmg = dmg * 2
            self.rage += 1
        else:
            now_dmg = dmg
            self.rage += 1
        self.take_damage(now_dmg)
        return now_dmg


class Magician(Character):
    def __init__(self, name):
        super().__init__(name, hp=1, attack=5, defense=2, creet_chans=8, mana=50, max_mana=100)

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet = random.randint(1, 100)
        if creet <= self.creet_chans:
            now_dmg = dmg * 2
        else:
            now_dmg = dmg

        if self.mana >= 50:
            activation = input('включить супер атаку(1)')
            if activation == 1:
                now_dmg = dmg * 3
                self.mana -= 50

        self.mana_regen()
        self.take_damage(now_dmg)
        return now_dmg

    def mana_regen(self):
        self.mana += 7
        if self.mana >= 50:
            print(f'у игрока{self.name} {self.mana} маны')

    # вызываем add_max_mana через проверку isinstance в функции битвы
    def add_max_mana(self):
        level = 0
        if self.level >= level:
            self.level = level
            self.max_mana += 25


class Archer(Character):
    def __init__(self, name):
        super().__init__(name, hp=3, attack=4, defense=3, creet_chans=17)
        self.accuracy = 10

    def get_attack_power(self):
        return self.attack

    def attack_target(self, target):
        dmg = self.get_attack_power()
        creet = random.randint(1, 100)
        accuracy_func = random.randint(1, 100)
        add_dmg = 0
        if accuracy_func <= self.accuracy:
            add_dmg = dmg + dmg
        if creet <= self.creet_chans:
            now_dmg = dmg * 2 + add_dmg
        else:
            now_dmg = dmg
        self.take_damage(now_dmg)
        return now_dmg

    # вызываем add_accuracy через проверку isinstance в функции битвы
    def add_accuracy(self):
        level = 0
        if self.level >= level:
            self.level = level
            self.accuracy += 2


class HealingPotion(Item):
    def __init__(self, amount=4):
        super().__init__(f'зелье здоровья (+{amount} hp)',
                         f"Редкая гадость:  острый перец и фарментированые (гнилые) помидоры (восстанавливает {amount} hp).")
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
        super().__init__(f'зелье маны (+{amount} hp)', f'востанавливает {amount} маны')
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
        print('создание персонажа из нечего (просто порох взорвался)')

        while True:
            chose_player = input('ведите 1 чтобы выбрать лучника , 2 чтоб мага и 3 чтоб воина')
            if chose_player == '1':
                name = input('скажите ваше ИМЯ НЕМЕДЛЕНО')
                self.player = Archer(name)
                print(f'ВЫ СОЗДАЛИ ЛУЧНИКА С ИМЕНЕМ {self.player.name}')
                break
            elif chose_player == '2':
                name = input('скажите ваше ИМЯ НЕМЕДЛЕНО')
                self.player = Magician(name)
                print(f'ВЫ СОЗДАЛИ МАГА С ИМЕНЕМ {self.player.name}')
                break
            elif chose_player == '3':
                name = input('скажите ваше ИМЯ НЕМЕДЛЕНО')
                self.player = Warrior(name)
                print(f'ВЫ СОЗДАЛИ ВОИНА С ИМЕНЕМ {self.player.name}')
                break
            else:
                print(f'Я СКАЗАЛ 123, а не {chose_player}!')
        print(self.player)

    def spawn_enemy(self):
        enemy = [EnemyOnBackOfTheClass, AngryTeacher]
        chose_enemy = random.choice(enemy)
        self.enemy = chose_enemy()
        print(f'На вас {self.enemy.name} напал  и у него {self.enemy}')

    def battle(self):
        self.count += 1
        print(f'битва началась {self.count}')
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_player()
            if self.enemy.is_alive():
                self.turn_enemy()
            if not self.enemy.is_alive() :
                self.end_battle()
            if not self.player.is_alive() :
                break

    def turn_player(self):
        while True:

            print('1 атака,2 просмотр инветаря,3 использовать предмет из инвентаря,4 побег')
            player_chose = int(input('ведите число'))
            if player_chose == 1:
                dmg = self.player.attack_target(self.enemy)
                print(f'Вы нанесли {dmg} урона!')
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
        pass

    def use_item(self):
        pass

    def end_battle(self):
        pass
