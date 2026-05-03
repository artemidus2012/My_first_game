import random
import time
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, attack, defense, exp, level, creet_chans,max_hp):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
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
        super().__init__(name, hp=1, attack=5, defense=2, creet_chans=8)
        self.mana = 50
        self.max_mana = 100

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
    def __init__(self,amount = 4):
        super().__init__(f'зелье здоровья (+{amount} hp)',f"(восстанавливает {amount} hp)")
        self.amount = amount
    def use(self, character) :
        max_hp = character.max_hp
        character.hp += self.amount
        if character.hp > max_hp :
            character.hp = max_hp