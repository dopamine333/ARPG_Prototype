from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Camera.Camera import Camera
from pygame import Rect, Vector2, Vector3
from Scripts.GameObject.GameObject import GameObject
from Scripts.GameObject.Component import Component


class CameraController(Component):
    '''
    跟隨一個遊戲物件(GameObject)

    可設定跟隨軸向和設定活動範圍

    屬性:
        offset: Vector = (0,0,0)
        follow_speed: float = 0.8 in range [0, 1]
        follow_axis: tuple[bool,bool,bool] = (True, True, True)
    '''

    def __init__(self) -> None:
        super().__init__()
        self.target: GameObject = None
        self.offset = Vector3()
        self.follow_axis = (True, True, True)
        self.follow_speed = 0.3

        self.camera: Camera = None

    def start(self):
        self.camera = self.get_component(Camera)
        if self.target:
            self.position.xyz = self.target.position+self.offset
    # region setter

    def set_target(self, target: GameObject):
        self.target = target
        self.position.xyz = self.target.position+self.offset

    def set_offset(self, offset: Vector3):
        self.offset = Vector3(offset)

    def set_follow_speed(self, follow_speed: float):
        self.follow_speed = follow_speed

    def set_follow_axis(self, x=True, y=True, z=True):
        self.follow_axis = (x, y, z)
    # endregion        

    def update(self):
        if self.target:
            old_position = self.position.xyz
            self.position.xyz=self.position.lerp(self.target.position+self.offset, self.follow_speed)
            if not self.follow_axis[0]:
                self.position.x = old_position.x
            if not self.follow_axis[1]:
                self.position.y = old_position.y
            if not self.follow_axis[2]:
                self.position.z = old_position.z
