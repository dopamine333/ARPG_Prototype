import pygame
import pygame.event
from Scripts.Managers.EventManager import Event,EventManager
class InputProcessor:
    def process(self,event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                EventManager.notify(Event.press_down_space)
            if event.key ==pygame.K_s:
                EventManager.notify(Event.start_Battle)
            if event.key ==pygame.K_e:
                EventManager.notify(Event.end_Battle)

