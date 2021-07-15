from Scripts.Locals import Face
from pygame import Vector3


class Box:
    '''描述三維空間中的一個長方體'''

    def __init__(self, size: Vector3, center: Vector3) -> None:
        self.size = Vector3(size)
        self.center = Vector3(center)

    def get_size(self):
        return self.size

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
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
