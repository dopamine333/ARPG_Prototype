import pygame
import pygame.event
from pygame.event import Event
from Scripts.Managers.EventManager import EventManager


class InputProcessor:
    def process(self, event: Event):
        pass
        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                EventManager.notify(Event.press_down_space)
            if event.key ==pygame.K_s:
                EventManager.notify(Event.start_Battle)
            if event.key ==pygame.K_e:
                EventManager.notify(Event.end_Battle)
'''
