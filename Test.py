if __name__!="__main__":
    print("???")
from math import sin
import pygame
from time import time
import pygame.time
import pygame.event
import pygame.display
import pygame.key

class AttackParam:
    def __init__(self, damage) -> None:
        self.damage = damage
        self.attacker = None
        self.defender = None

    def set_attacker(self, attacker):
        self.attacker = attacker

    def set_defender(self, defender):
        self.defender = defender
class Buffer:
    def __init__(self) -> None:
        self.items: dict[str, float] = {}
        self.lasttime = 0

    def update(self):
        deltatime = time()-self.lasttime
        self.lasttime = time()

        to_del = []
        for name in self.items.keys():
            if self.items[name] <= 0:
                to_del.append(name)
                continue
            self.items[name] -= deltatime
        for name in to_del:
            del self.items[name]

    def set(self, name: str, timeleft: float):
        if timeleft>0:
            self.items[name] = timeleft

    def get(self, name: str):
        return name in self.items

    def pop(self, name: str):
        if name in self.items:
            del self.items[name]
            return True
        return False



class Brain:
    def __init__(self) -> None:
        self.character: Character = None

    def update(self):
        pass



class Character:
    def __init__(self) -> None:
        self.maxhp = 10
        self.hp = self.maxhp
        self.position=0
        self.name="no name"
        self.brain: Brain = None
    def set_name(self,name):
        self.name=name
    
    def set_brain(self,brain):
        self.brain=brain
        self.brain.character=self

    def update(self):
        self.brain.update()

    def underattack(self, attackparam: AttackParam):
        self.hp -= attackparam.damage
        if self.hp < 0:
            self.dead()

    def dead(self):
        print(self.name)
class Cat(Character):
    def __init__(self) -> None:
        super().__init__()

    def meow(self):
        print(self.name,"meow~","im in",self.position)

    def move(self,direction):
        self.position+=direction

class TimeCatBrain(Brain):
    def __init__(self) -> None:
        super().__init__()
        self.lastmeow=0
        
    def update(self):
        if time()-self.lastmeow>2:
            self.character.meow()
            self.character.move(1)
            self.lastmeow=time()

class InputCatBrain(Brain):
    def update(self):
        if pygame.key.get_pressed()[pygame.K_m]:
            self.character.move(-1)
            self.character.meow()


               
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((100, 100))
c=Cat()
tcb=TimeCatBrain()
c.set_brain(tcb)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                import sys
                sys.exit()
            if event.key == pygame.K_t:
                c.set_brain(TimeCatBrain())
            if event.key == pygame.K_i:
                c.set_brain(InputCatBrain())
            
    c.update()
