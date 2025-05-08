from asyncio.windows_events import NULL
from random import randint
import random


class Character:
    __id = 0
    
    def __init__(self, team):
        Character.__id += 1
        self.id = Character.__id
        self.team = team
    
    def __del__(self):
        print(f'Char {self.id} deleted')

class Hero(Character):
    def __init__(self, team):
        super().__init__(team)
        self.level = 0
        self.lst = []
    def increase_level(self):
        self.level += 1
        random.choice(self.lst).follow_by_hero(self)

class Solider(Character):
    def follow_by_hero(self, hero):
        print(f'Follow by {hero.id}')

hero1 = Hero('Teutonic')
hero2 = Hero('Livonian')
for sol in range(randint(10, 20)):
    hero1.lst.append(Solider(hero1.team)) if randint(0, 1) else hero2.lst.append(Solider(hero2.team))

hero1.increase_level() if len(hero1.lst) > len(hero2.lst) else hero2.increase_level()
print(hero1.level)
print(hero2.level)

del hero2