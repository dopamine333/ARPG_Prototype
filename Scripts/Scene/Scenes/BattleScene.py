import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import Event,EventManager

class BattleScene(Scene):
    def start(self):
        print("Battle Time start!!!")
        EventManager.attach(Event.end_Battle,self.to_mainmenu)  

    def end(self):
        print("battle end!")
        EventManager.detach(Event.end_Battle,self.to_mainmenu)  

    def to_mainmenu(self):
        print("go to mainmenu !!!")
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)