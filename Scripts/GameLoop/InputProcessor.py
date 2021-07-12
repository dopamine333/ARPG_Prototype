from Scripts.Locals import InputEvent
import pygame
import pygame.event
from pygame.event import Event
from Scripts.Managers.EventManager import EventManager


class InputProcessor:
    def process(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_j:
                EventManager.notify(InputEvent.key_down,InputEvent.fire)
            if event.key ==pygame.K_SPACE:
                EventManager.notify(InputEvent.key_down,InputEvent.jump)
            if event.key ==pygame.K_k:
                EventManager.notify(InputEvent.key_down,InputEvent.jump)
        if event.type==pygame.MOUSEBUTTONDOWN:
            EventManager.notify(InputEvent.key_down,InputEvent.fire)
