
import pygame
from Scripts.EventManager.EventManager import EventManager
from pygame import Vector2
from Scripts.Locals import InputEvent
from Scripts.Character.CharacterBrain.CharacterBrain import CharacterBrain
import pygame.key


class PlayerController(CharacterBrain):
    def start(self):
        EventManager.attach(InputEvent.move_down, self.move_down)
        EventManager.attach(InputEvent.move_up, self.move_up)
        EventManager.attach(InputEvent.move_right, self.move_right)
        EventManager.attach(InputEvent.move_left, self.move_left)
        EventManager.attach(InputEvent.fire, self.attack)
        EventManager.attach(InputEvent.jump, self.jump)
        #EventManager.attach(InputEvent.dash, self.dash)

    def end(self):
        EventManager.detach(InputEvent.move_down, self.move_down)
        EventManager.detach(InputEvent.move_up, self.move_up)
        EventManager.detach(InputEvent.move_right, self.move_right)
        EventManager.detach(InputEvent.move_left, self.move_left)
        EventManager.detach(InputEvent.fire, self.attack)
        EventManager.detach(InputEvent.jump, self.jump)
        #EventManager.detach(InputEvent.dash, self.dash)
    def __init__(self) -> None:
        super().__init__()
        self.movement=Vector2()
        self.do_jump=False
        self.do_attack=False
        #self.do_dash=False
    def update(self):
        if self.movement.xy!=(0,0):
            self.character.move(self.movement)
            self.movement.xy=(0,0)
            self.do_move=False
        if self.do_jump:
            self.character.jump()
            self.do_jump=False
        if self.do_attack:
            self.character.attack()
            self.do_attack=False
    def move_up(self):
        self.movement += Vector2(0, 1)

    def move_down(self):
        self.movement += Vector2(0, -1)

    def move_left(self):
        self.movement += Vector2(-1, 0)

    def move_right(self):
        self.movement += Vector2(1, 0)

    def jump(self):
        self.do_jump=True
    #def dash(self):
    #    self.character.dash()

    def attack(self):
        self.do_attack=True
