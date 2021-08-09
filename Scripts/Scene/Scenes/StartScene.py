from Scripts.GameSystem.GameManager import GameManager
from Scripts.GameObject.GameObject import GameObject
from Scripts.Scene.Scenes.MainMenuScene import MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene


class StartScene(Scene):
    def scene_start(self):

        # FIXME 在哪裡載入關卡
        from Data.LevelData import LevelData1
        GameManager.Instance().add_level(LevelData1.read(), 1)

    def start(self):
        super().start()
        self.to_mainmenu()

    def to_mainmenu(self):
        self.change_scene(MainMenuScene)
