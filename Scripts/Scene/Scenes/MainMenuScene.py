from Scripts.GameSystem.GameManager import GameManager
from Scripts.Button.MouseManager import MouseManager
from Scripts.Graphic.Render.Render import Render
from Scripts.GameObject.GameObject import GameObject
from Scripts.Button.Button import Button
from Scripts.Graphic.Image import Image
from Scripts.Locals import ButtonEvent, Layer
from pygame.image import load
import Scripts.Scene.Scenes.BattleScene
from Scripts.Scene.Scenes.Scene import Scene


class MainMenuScene(Scene):
    def on_load(self):

        play_button_source = load(
            r"Arts\MainMenu\play_button.png").convert_alpha()
        play_button_size = play_button_source.get_size()
        play_button = GameObject()
        play_button_render = play_button.add_component(Render)
        play_button_button = play_button.add_component(Button)
        play_button_render.set_image(Image(play_button_source))
        play_button_render.set_layer(Layer.UI)
        play_button_button.set_button_size(play_button_size)
        play_button.set_position((640, 400, 0))

        game_title_source = load(
            r"Arts\MainMenu\game_title.png").convert_alpha()
        game_title = GameObject()
        game_title_render: Render = game_title.add_component(Render)
        game_title_render.set_image(Image(game_title_source))
        game_title_render.set_layer(Layer.UI)
        game_title.set_position((640, 200, 0))

        play_button_button.get_button_event(ButtonEvent.up) + self.to_battle

        self.instantiate(play_button, game_title)

    def to_battle(self):
        # FIXME 選擇關卡
        GameManager.Instance().choice_level(1)
        self.change_scene(Scripts.Scene.Scenes.BattleScene.BattleScene)
