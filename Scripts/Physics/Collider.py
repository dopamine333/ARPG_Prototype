from Scripts.Locals import Face
from pygame import Vector3


class Collider:
    '''剛體(RigidBody)的碰撞箱'''

    def __init__(self, size: Vector3, center: Vector3) -> None:
        self.size = Vector3(size)
        self.center = Vector3(center)
        self.surfaces: dict[Face, float] = {
            Face.up: self.size.y-self.center.y,
            Face.down: -self.center.y,
            Face.right: self.size.x-self.center.x,
            Face.left: -self.center.x,
            Face.front: self.size.z-self.center.z,
            Face.back: -self.center.z
        }

    def get_size(self):
        return self.size

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
        return self.surfaces[face]