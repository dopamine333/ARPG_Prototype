from Scripts.Scene.Scenes.StartScene import StartScene
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
        self.running = False

        self.input_manager = InputManager()
        MouseManager.init()
        Physics.init()
        SceneManager.change_scene(StartScene())
        RenderManager.set_screen(self.screen)

    def run(self):
        '''遊戲開始，迴圈啟動。'''
        self.running = True
        while self.running:
            self.initialization()

            self.physics()
            self.input_events()
            self.game_logic()
            self.rendering()
            self.end_of_frame()
            
            self.decommissioning()
        
        self.quit()

    def initialization(self):
        SceneManager.initialization()


    def physics(self):
        SceneManager.physics()

    def input_events(self):
        for event in pygame.event.get():
            # 處理事件，如果是退出則結束遊戲，其餘交給InputManager處理
            if event.type == pygame.QUIT:
                self.running = False
            self.input_manager.process(event)
        self.input_manager.update()
        MouseManager.update()

    def game_logic(self):
        SceneManager.update()

    def rendering(self):
        #on_will_render_object
        SceneManager.rendering()
        #on_render_object
        RenderManager.render()
        #on_render_image
        pygame.display.update()

    def end_of_frame(self):
        # 固定幀率(Frame Per Second; fps)為60
        Time.tick()

    def decommissioning(self):
        SceneManager.decommissioning()

    def quit(self):
        pygame.quit()
        sys.exit()