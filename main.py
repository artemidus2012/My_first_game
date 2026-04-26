import random
import time
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, attack, defense, exp, level, creet_chans):
        self.name = name
        self.hp = hp
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
        self.hp += 2
        self.defense += 2
        self.exp = 0
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
        return f'твоё имя - {self.name} у вас {self.hp} здоровьья вы бьёте с силой {self.attack} у вас такая защита {self.defense} у вас столко опыта {self.exp}и вы на {self.level} левле'


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
            target.hp -= dmg * 2 * 2
            self.rage += 1
        elif self.rage == 50 or creet <= self.creet_chans:
            target.hp -= dmg * 2
        else:
            target.hp -= dmg
            self.rage += 1
