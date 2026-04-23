import random
import time
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, attack, defense, exp, level):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.level = level
        self._inventory = []

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

    def level_up (self) :
       self.level += 1
       self.attack += 2
       self.hp += 2
       self.defense += 2
       self.exp = 0
       print(f'персонаж {self.name} повышает уровень до {self.level} и повышает характеристики : здоровье {self.hp},урон{self.attack},зашита{self.defense}')