from Scripts.Scene.Scenes.MainMenuScene import MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import Event,EventManager

class StartScene(Scene):
    def start(self):
        print("start of start!!!")
        self.to_mainmenu()
    def end(self):
        print("end of start!")
    def to_mainmenu(self):
        print("go to mainmenu !!!")
        self.change_scene(MainMenuScene)