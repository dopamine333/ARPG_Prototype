from Scripts.GameSystem.GameManager import GameManager
from Scripts.Scene.Scenes.MainMenuScene import MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene


class StartScene(Scene):
    def on_load(self):
        print("StartScene:on_load")
        # FIXME 在哪裡載入關卡
        from Data.LevelData import LevelData1
        GameManager.Instance().add_level(LevelData1.read(), 1)

    def on_instantiate(self):
        self.change_scene(MainMenuScene)

