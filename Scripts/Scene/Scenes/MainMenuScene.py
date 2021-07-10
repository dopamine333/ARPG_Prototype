from Scripts.Locals import ButtonEvent
from Scripts.GameObject.UI.UI import UI
from pygame.image import load
from Scripts.Graph.Image import Image
from Scripts.GameObject.UI.Button import Button
import Scripts.Scene.Scenes.BattleScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import EventManager


class MainMenuScene(Scene):
    def init(self):
        play_button_source = load(
            r"Arts\MainMenu\play_button.png").convert_alpha()
        play_button_rect = play_button_source.get_rect()
        play_button_rect.center = (640, 400)
        self.play_button = Button(Image(play_button_source), play_button_rect)

        game_title_source = load(
            r"Arts\MainMenu\game_title.png").convert_alpha()
        game_title = UI(Image(game_title_source), (640, 200))

        self.play_button.attach(ButtonEvent.down, self.to_battle)

        self.add_gameobjects(self.play_button, game_title)

    def start(self):
        print("ssss")
        return super().start()

    def release(self):
        self.play_button.detach(ButtonEvent.down, self.to_battle)

    def to_battle(self):
        print("MainMenuScene:go to battle!")
        self.change_scene(Scripts.Scene.Scenes.BattleScene.BattleScene)
