import pygame
from time import time
import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import EventManager


class BattleScene(Scene):
    def init(self):
        self.start_time = time()

    def update(self):
        print(f"battling !! {time()-self.start_time}")
        if(time()-self.start_time > 10):
            self.to_mainmenu()

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
