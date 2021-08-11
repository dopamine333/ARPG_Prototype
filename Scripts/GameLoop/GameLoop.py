from Scripts.Time.Time import Time
from Scripts.Physics.Physics import Physics
from Scripts.Button.MouseManager import MouseManager
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.GameLoop.InputManager import InputManager
import pygame
import pygame.display
import pygame.time
import pygame.event
import sys
from pygame import Vector2
from Scripts.Scene.SceneManager import SceneManager


class GameLoop:
    '''
    遊戲主迴圈，

    呼叫RenderManager、Physics、MouseManager更新，

    委派InputManager處理輸入。
    '''

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_size = Vector2(self.screen.get_size())
        Time.set_target_fps(60)

        self.input_manager = InputManager()
        MouseManager.init()
        Physics.init()
        RenderManager.set_screen(self.screen)

    def run(self):
        '''
        遊戲開始，迴圈啟動。
        '''
        running = True
        while running:
            # 固定幀率(Frame Per Second; fps)為60
            Time.tick()
            # print(self.clock.get_fps())
            self.update()
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                # 處理事件，如果是退出則結束遊戲，其餘交給InputManager處理
                if event.type == pygame.QUIT:
                    running = False
                self.input_event_process(event)
        pygame.quit()
        sys.exit()

    def input_event_process(self, event):
        self.input_manager.process(event)

    def draw(self):
        RenderManager.render()

    def update(self):
        self.input_manager.update()
        SceneManager.update()
