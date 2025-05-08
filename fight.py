import random


class Warior:
    age = 0
    def __init__(self, name):
        self.health = 100
        self.name = name
    def go(self, side):
        return(f'{self.name} goes to {side}')
    def fight(self, enemy):
        enemy.health -= 20
        return(f'{enemy.name} was attacked by {self.name}. {enemy.name}\'s was encrease to {enemy.health}.')
    

warior1 = Warior('Ivan')
print(warior1.__dict__)
print(warior1.age)
warior1.age = 20
print(warior1.__dict__)
print(warior1.go('right'))
warior2 = Warior('Vlad')
while warior1.health > 0 and warior2.health > 0:
    rnd = random.randint(1, 2)
    print(warior1.fight(warior2)) if rnd == 1 else print(warior2.fight(warior1))
winner = warior2 if warior1.health <= 0 else warior1
print(f'{winner.name} win!')
