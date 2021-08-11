
from Scripts.Time.Time import Time
from pygame import mouse
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
    def __init__(self) -> None:
        self.move_up=EventManager.get(InputEvent.move_up)
        self.move_down=EventManager.get(InputEvent.move_down)
        self.move_left=EventManager.get(InputEvent.move_left)
        self.move_right=EventManager.get(InputEvent.move_right)
        self.fire=EventManager.get(InputEvent.fire)
        self.jump=EventManager.get(InputEvent.jump)
        self.change_collision_type=EventManager.get(InputEvent.change_collision_type)

    def update(self):
        '''
        處理｢按住｣的事件
        '''
        if Time.is_paused():
            return
        # WASD或上下左右件都能觸發移動事件
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            self.move_up.notify()
        if key_input[pygame.K_s]:
            self.move_down.notify()
        if key_input[pygame.K_a]:
            self.move_left.notify()
        if key_input[pygame.K_d]:
            self.move_right.notify()
        if key_input[pygame.K_UP]:
            self.move_up.notify()
        if key_input[pygame.K_DOWN]:
            self.move_down.notify()
        if key_input[pygame.K_LEFT]:
            self.move_left.notify()
        if key_input[pygame.K_RIGHT]:
            self.move_right.notify()

    def process(self, event: Event):
        '''
        處理｢按下｣的事件
        '''
        if Time.is_paused():
            return
        # J或滑鼠左鍵攻擊
        # K或空白鍵跳躍
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.fire.notify()
            if event.key == pygame.K_SPACE:
                self.jump.notify()
            if event.key == pygame.K_k:
                self.jump.notify()
            '''if event.key == pygame.K_l:
                EventManager.notify(InputEvent.dash)'''
            if event.key == pygame.K_p:
                self.change_collision_type.notify()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed=mouse.get_pressed()
            if pressed[0]:
                self.fire.notify()
            '''if pressed[2]:
                EventManager.notify(InputEvent.dash)'''
