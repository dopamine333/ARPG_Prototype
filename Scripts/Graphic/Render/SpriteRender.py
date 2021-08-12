from Scripts.Locals import Face
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
        self.face: Face = Face.right
        # TODO 想一下翻轉圖片要放在哪比較好

    def set_shadow_size(self, shadow_size: Vector2):
        self.shadow_size = Vector2(shadow_size)

    def set_face(self, face: Face):
        self.face = face

    def on_will_render_object(self):
        RenderManager.camera.draw(
            self.image.flip(True, False) \
                if self.face == Face.left else self.image,
            self.gameobject.position,
            self.shadow_size
        )
