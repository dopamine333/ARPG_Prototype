from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.Collider import Collider

from Scripts.Physics.Collision import Collision
from Scripts.Managers.PhysicsManager import PhysicsManager
from Scripts.Locals import Face, GRAVITY
from pygame import Vector3
from Scripts.GameObject.Sprite.Sprite import Sprite
import pygameEngine
import math

#TODO 完成RigidBody的類別圖

class RigidBody:
    def __init__(self, collider: Collider, apply_gravity: bool = True) -> None:
        self.collider = collider
        self.sprite: Sprite = None

        self.position = Vector3()
        self.velocity = Vector3()
        self.acceleration = Vector3()

        self.apply_gravity = apply_gravity
        self.horizontal_max_speed = math.inf
        self.horizontal_max_speed_squared = math.inf
        self.damp = 1
    #TODO 移動最高速度而不是水平最高速度
    def set_horizontal_max_speed(self, horizontal_max_speed):
        self.horizontal_max_speed = horizontal_max_speed
        self.horizontal_max_speed_squared = horizontal_max_speed**2

    def set_damp(self, damp: float):
        self.damp = damp

    def set_sprite(self, sprite: Sprite):
        self.sprite = sprite
        self.position = sprite.get_position()

    def get_collider(self):
        return self.collider

    def start(self):
        PhysicsManager.Instance().attach(self)

    def end(self):
        PhysicsManager.Instance().detach(self)
    def update(self):
        if self.apply_gravity:
            self.acceleration.y += GRAVITY

        self.velocity += self.acceleration
        self.velocity *= self.damp
        if self.velocity.xz.length_squared() > self.horizontal_max_speed_squared:
            vxz=self.velocity.xz
            vxz.scale_to_length(self.horizontal_max_speed)
            self.velocity.xz=vxz
        self.position += self.velocity
        self.acceleration.xyz = (0, 0, 0)

        PhysicsManager.Instance().check(self)

    def add_force(self, force: Vector3):
        self.acceleration += force

    def get_surface(self, face: Face):
        collider_surface = self.collider.get_surface(face)
        if face == Face.up or face == Face.down:
            return collider_surface+self.position.y
        if face == Face.right or face == Face.left:
            return collider_surface+self.position.x
        if face == Face.back or face == Face.front:
            return collider_surface+self.position.z

    def set_surface(self, face: Face, value: float):
        collider_surface = self.collider.get_surface(face)
        if face == Face.up:
            self.position.y = value-collider_surface
        elif face == Face.down:
            self.position.y = value-collider_surface
        elif face == Face.right:
            self.position.x = value-collider_surface
        elif face == Face.left:
            self.position.x = value-collider_surface
        elif face == Face.front:
            self.position.z = value-collider_surface
        elif face == Face.back:
            self.position.z = value-collider_surface

    def collide(self,collision:Collision):
        self.sprite.collide(collision)