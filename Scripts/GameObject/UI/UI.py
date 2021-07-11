from Scripts.Locals import Layer
from Scripts.Graph.Image import Image
from pygame import Vector2
from Scripts.GameObject.GameObject import GameObject
from Scripts.Graph.Render import Render


class UI(GameObject):
    def __init__(self, image: Image, UI_position: Vector2) -> None:
        super().__init__()
        self.UI_position = UI_position
        self.image = image

    def draw(self, render: Render):
        render.draw(self.image, self.UI_position,Layer.UI)
