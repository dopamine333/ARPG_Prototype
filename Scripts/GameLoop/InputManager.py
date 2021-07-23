from random import uniform

from pygame import mouse
from Scripts.Button.MouseManager import MouseManager
from Scripts.Locals import InputEvent
import pygame
import pygame.event
from pygame.event import Event
from Scripts.EventManager.EventManager import EventManager
import pygame.key


class InputManager:
    '''
    處理輸入事件並通知EventManager
    '''

    def update(self):
        '''
        處理｢按住｣的事件
        '''
        # WASD或上下左右件都能觸發移動事件
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            EventManager.notify(InputEvent.move_up)
        if key_input[pygame.K_s]:
            EventManager.notify(InputEvent.move_down)
        if key_input[pygame.K_a]:
            EventManager.notify(InputEvent.move_left)
        if key_input[pygame.K_d]:
            EventManager.notify(InputEvent.move_right)
        if key_input[pygame.K_UP]:
            EventManager.notify(InputEvent.move_up)
        if key_input[pygame.K_DOWN]:
            EventManager.notify(InputEvent.move_down)
        if key_input[pygame.K_LEFT]:
            EventManager.notify(InputEvent.move_left)
        if key_input[pygame.K_RIGHT]:
            EventManager.notify(InputEvent.move_right)

    def process(self, event: Event):
        '''
        處理｢按下｣的事件
        '''
        # J或滑鼠左鍵攻擊
        # K或空白鍵跳躍
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                EventManager.notify(InputEvent.fire)
            if event.key == pygame.K_SPACE:
                EventManager.notify(InputEvent.jump)
            if event.key == pygame.K_k:
                EventManager.notify(InputEvent.jump)
            if event.key == pygame.K_l:
                EventManager.notify(InputEvent.dash)
            if event.key == pygame.K_p:
                EventManager.notify(InputEvent.change_collision_type)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed=mouse.get_pressed()
            if pressed[0]:
                EventManager.notify(InputEvent.fire)
            if pressed[2]:
                EventManager.notify(InputEvent.dash)
