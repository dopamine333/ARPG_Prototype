from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Locals import Layer
from Scripts.GameObject.Component import Component
from Scripts.Graphic.Image import Image


class Render(Component):
    '''
    負責與RenderManager溝通的組件(Component)

    屬性:
        +image: Image
        -layer: Layer
    '''

    def __init__(self) -> None:
        super().__init__()
        self.image: Image = None
        self.layer: Layer = None

    def set_image(self, image: Image):
        self.image = image

    def set_layer(self, layer: Layer):
        self.layer = layer

    def update(self):
        if self.image and self.layer:
            RenderManager.draw(
                self.image, self.gameobject.position.xy, self.layer)
