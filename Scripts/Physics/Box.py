from Scripts.Locals import Face
from pygame import Vector3


class Box:
    def __init__(self,center:Vector3,size:Vector3) -> None:
        self.center = Vector3 (center)
        self.size = Vector3( size)

    def get_size(self):
        return self.size

    def get_surface(self, face: Face):
        if face == Face.up:
            return self.center.y+self.size.y/2
        if face == Face.down:
            return self.center.y-self.size.y/2
        if face == Face.right:
            return self.center.x+self.size.x/2
        if face == Face.left:
            return self.center.x-self.size.x/2
        if face == Face.front:
            return self.center.z+self.size.z/2
        if face == Face.back:
            return self.center.z-self.size.z/2
