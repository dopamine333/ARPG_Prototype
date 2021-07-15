from Scripts.Locals import Face
from pygame import Vector3


class Collider:
    '''剛體(RigidBody)的碰撞箱'''

    def __init__(self, size: Vector3, center: Vector3) -> None:
        self.size = Vector3(size)
        self.center = Vector3(center)

    def get_size(self):
        return self.size

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
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
