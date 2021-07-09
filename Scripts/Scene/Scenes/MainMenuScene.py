import Scripts.Scene.Scenes.BattleScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import Event,EventManager
class MainMenuScene(Scene):
    def start(self):
        print("MainMenu start~~~")
        EventManager.attach(Event.start_Battle,self.to_battle)  
    def end(self):
        print("MainMenu end!")
        EventManager.detach(Event.start_Battle,self.to_battle)  

    def to_battle(self):
        print("go to battle !!!")
        self.change_scene(Scripts.Scene.Scenes.BattleScene.BattleScene)
