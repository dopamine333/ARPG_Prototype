from Scripts.Locals import InputEvent
import pygame
import pygame.event
from pygame.event import Event
from Scripts.Managers.EventManager import EventManager


class InputProcessor:
    def process(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_j:
                EventManager.notify(InputEvent.key_down,InputEvent.j)
            if event.key ==pygame.K_SPACE:
                EventManager.notify(InputEvent.key_down,InputEvent.j)
            if event.key ==pygame.K_k:
                EventManager.notify(InputEvent.key_down,InputEvent.k)

