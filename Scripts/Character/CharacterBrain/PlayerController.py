
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

    def end(self):
        EventManager.detach(InputEvent.move_down, self.move_down)
        EventManager.detach(InputEvent.move_up, self.move_up)
        EventManager.detach(InputEvent.move_right, self.move_right)
        EventManager.detach(InputEvent.move_left, self.move_left)
        EventManager.detach(InputEvent.fire, self.attack)
        EventManager.detach(InputEvent.jump, self.jump)

    def move_up(self):
        self.character.move(Vector2(0, 1))

    def move_down(self):
        self.character.move(Vector2(0, -1))

    def move_left(self):
        self.character.move(Vector2(-1, 0))

    def move_right(self):
        self.character.move(Vector2(1, 0))

    def jump(self):
        self.character.jump()

    def attack(self):
        self.character.attack()
