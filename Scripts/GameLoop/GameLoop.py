from Scripts.Graph.Render import Render
import pygame
import pygame.display
import pygame.time
import pygame.event
import sys
from pygame import Vector2
from Scripts.Graph.Camera import Camera
from Scripts.Scene.SceneChanger import SceneChanger
from Scripts.GameLoop.InputProcessor import InputProcessor
from Scripts.Managers.MouseManager import MouseManager
from Scripts.Managers.PhysicsManager import PhysicsManager


class GameLoop:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        self.screen_size = Vector2(self.screen.get_size())
        self.clock = pygame.time.Clock()

        self.input_processor = InputProcessor()
        self.render = Render(self.screen)
        self.scene_changer = SceneChanger()

    def run(self):
        '''start the game'''
        running = True
        while running:
            self.clock.tick(60)
            self.update()
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.input_process(event)
        pygame.quit()
        sys.exit()

    def input_process(self, event):
        self.input_processor.process(event)

    def draw(self):
        self.scene_changer.draw(self.render)
        self.render.render()

    def update(self):
        MouseManager.Instance().update()
        self.scene_changer.update()
