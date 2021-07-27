from __future__ import annotations
from Scripts.Locals import Face
from pygame import Vector3


class Box:
    '''描述三維空間中的一個長方體'''

    def __init__(self, size: Vector3, center: Vector3) -> None:
        self.size = Vector3(size)
        self.half_size = self.size*0.5
        self.center = Vector3(center)
        self.surfaces: dict[Face, float] = {
            Face.up: self.center.y+self.half_size.y,
            Face.down: self.center.y-self.half_size.y,
            Face.right: self.center.x+self.half_size.x,
            Face.left: self.center.x-self.half_size.x,
            Face.front: self.center.z+self.half_size.z,
            Face.back: self.center.z-self.half_size.z
        }

    def get_size(self):
        return self.size

    def set_size(self, size: Vector3):
        self.size = Vector3( size)
        self.half_size = self.size*0.5

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
        return self.surfaces[face]

    def union(self, other_box: Box):
        size = (max(self.get_surface(Face.right)-other_box.get_surface(Face.left),
                    other_box.get_surface(Face.right)-other_box.get_surface(Face.left)),
                max(self.get_surface(Face.up)-other_box.get_surface(Face.down),
                    other_box.get_surface(Face.up)-other_box.get_surface(Face.down)),
                max(self.get_surface(Face.front)-other_box.get_surface(Face.back),
                    other_box.get_surface(Face.front)-other_box.get_surface(Face.back)),)
        center=(0.5*(max(self.get_surface(Face.right),other_box.get_surface(Face.right))+\
                min(other_box.get_surface(Face.left),other_box.get_surface(Face.left))),
                0.5*(max(self.get_surface(Face.up),other_box.get_surface(Face.up))+\
                 min(other_box.get_surface(Face.down),other_box.get_surface(Face.down))),
                0.5*(max(self.get_surface(Face.front),other_box.get_surface(Face.front))+\
                min(other_box.get_surface(Face.back),other_box.get_surface(Face.back))))

        return Box(size,center)
     