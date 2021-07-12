from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.RigidBody import RigidBody
    from Scripts.Physics.Collision import Collision

from Scripts.Graph.Image import Image
from pygame import Vector3
from Scripts.GameObject.GameObject import GameObject
from Scripts.Graph.Render import Render


class Sprite(GameObject):
    def __init__(self, image: Image, position: Vector3, rigidbody: RigidBody) -> None:
        super().__init__()
        self.position = position
        self.image = image
        self.rigidbody = rigidbody
        self.rigidbody.set_sprite(self)

    def get_position(self):
        return self.position
    def draw(self, render: Render):
        render.camera.draw(self.image, self.position,self.rigidbody.get_collider().get_size().xz)
    
    def start(self):
        super().start()
        self.rigidbody.start()
    def update(self):
        super().update()
        self.rigidbody.update()
    def end(self):
        super().end()
        self.rigidbody.end()
    def collide(self,collision:Collision):
        pass
