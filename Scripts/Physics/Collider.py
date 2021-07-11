from Scripts.Locals import Face
from pygame import Vector3


class Collider:
    def __init__(self,center:Vector3,size:Vector3) -> None:
        self.center = center
        self.size = size

    def get_size(self):
        return self.size

    def get_surface(self, face: Face):
        if face == Face.up:
            return self.size.y-self.center.y
        if face == Face.down:
            return -self.center.y
        if face == Face.right:
            return self.size.x-self.center.x
        if face == Face.left:
            return -self.center.x
        if face == Face.front:
            return self.size.z-self.center.z
        if face == Face.back:
            return -self.center.z
