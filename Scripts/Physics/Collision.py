from Scripts.Locals import Face
from Scripts.GameObject.Sprite.Sprite import Sprite


class Collision:
    """
    描述一個碰撞事件
    """
    def __init__(self,sprite:Sprite,face:Face) -> None:
        self.sprite=sprite
        self.face=face
