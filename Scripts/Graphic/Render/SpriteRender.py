from pygame import Vector2
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Graphic.Render.Render import Render
from Scripts.GameObject.GameObject import GameObject


class SpriteRender(Render):
    '''
    繼承Render

    負責與RenderManager.camrea溝通的組件(Component)

    屬性:
        +image: Image
        -shadow_size: Vector2
    '''

    def __init__(self) -> None:
        super().__init__()
        self.shadow_size: Vector2 = None

    def set_shadow_size(self, shadow_size: Vector2):
        self.shadow_size = Vector2(shadow_size)

    def update(self):
        RenderManager.camera.draw(
            self.image, self.gameobject.position,
            self.shadow_size
        )
