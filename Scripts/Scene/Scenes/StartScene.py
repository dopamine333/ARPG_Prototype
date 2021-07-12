from Scripts.Scene.Scenes.MainMenuScene import MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import EventManager


class StartScene(Scene):
    def start(self):
        super().start()
        self.to_mainmenu()

    def to_mainmenu(self):
        self.change_scene(MainMenuScene)
