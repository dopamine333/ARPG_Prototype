from __future__ import annotations
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.Collision import Collision

from Scripts.Physics.Collider import Collider
from Scripts.Physics.Physics import Physics
from Scripts.GameObject.Component import Component
from Scripts.Locals import Face, ForceMode, GRAVITY
from pygame import Vector3

from Scripts.Tools.Action import Action

class RigidBody(Component):
    '''
    負責與Physics溝通的組件(Component)

    實現物理效果，並提供註冊的碰撞時呼叫某些方法的功能。

    屬性:
        -collider: Collider
        -damp: float = 1
        -apply_gravity: bool = True
        -frozen: bool = False
    '''

    def __init__(self) -> None:
        super().__init__()
        self.collider: Collider = None
        self.apply_gravity = True
        self.damp = 1
        self.frozen = False

        self.velocity = Vector3()
        self.acceleration = Vector3()
        self.surfaces: dict[Face, float] = {}
        self.on_collide_notify=Action()

    # region setter

    def set_collider(self, collider_size: Vector3, collider_center: Vector3):
        self.collider = Collider(collider_size, collider_center)
        # TODO daojdoiasjdoisjoid
        self.update_surface(Face.all)

    def set_frozen(self, frozen: bool):
        self.frozen = frozen

    def set_damp(self, damp: float):
        self.damp = damp

    def set_apply_gravity(self, apply_gravity: bool):
        self.apply_gravity = apply_gravity

    # endregion

    def start(self):
        Physics.attach(self)
        self.update_surface(Face.all)

    def end(self):
        Physics.detach(self)

    def update(self):
        # 更新物理
        if self.frozen:
            self.velocity.xyz = (0, 0, 0)
            return
        if self.apply_gravity:
            self.add_force(GRAVITY, ForceMode.force)
        self.velocity += self.acceleration
        self.velocity *= self.damp
        self.position += self.velocity*Physics.get_deltatime()  # 時間校正
        self.acceleration.xyz = (0, 0, 0)

        self.update_surface(Face.all)

        # 檢查碰撞
        Physics.check(self)

    def add_force(self, force: Vector3, force_mode: ForceMode = ForceMode.force):
        '''
        根據力種類不同選擇不同的力的模式(ForceMode)

        使在不同幀率(FPS)維持穩定的物理行為

        ForceMode.force   ->  施加一個持續的力時選擇

        ForceMode.impulse ->  施加一個瞬間的力時選擇
        '''
        if force_mode == ForceMode.force:
            self.acceleration += Vector3(force)*Physics.get_deltatime()  # 時間校正
        if force_mode == ForceMode.impulse:
            self.acceleration += Vector3(force)

    def update_surface(self, face: Face):
        if face == Face.all:
            self.surfaces[Face.up] = self.collider.get_surface(
                Face.up)+self.position.y
            self.surfaces[Face.down] = self.collider.get_surface(
                Face.down)+self.position.y
            self.surfaces[Face.front] = self.collider.get_surface(
                Face.front)+self.position.z
            self.surfaces[Face.back] = self.collider.get_surface(
                Face.back)+self.position.z
            self.surfaces[Face.right] = self.collider.get_surface(
                Face.right)+self.position.x
            self.surfaces[Face.left] = self.collider.get_surface(
                Face.left)+self.position.x
        else:
            if face in Face.rightleft:
                self.surfaces[Face.right] = self.collider.get_surface(
                    Face.right)+self.position.x
                self.surfaces[Face.left] = self.collider.get_surface(
                    Face.left)+self.position.x
            elif face in Face.updown:
                self.surfaces[Face.up] = self.collider.get_surface(
                    Face.up)+self.position.y
                self.surfaces[Face.down] = self.collider.get_surface(
                    Face.down)+self.position.y
            elif face in Face.frontback:
                self.surfaces[Face.front] = self.collider.get_surface(
                    Face.front)+self.position.z
                self.surfaces[Face.back] = self.collider.get_surface(
                    Face.back)+self.position.z

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
        return self.surfaces[face]

    def set_surface(self, face: Face, value: float):
        '''設定碰撞箱(Collider)不同面的座標，並改變位置(position)'''
        collider_surface = self.collider.get_surface(face)
        if face in Face.rightleft:
            self.position.x = value-collider_surface
        elif face in Face.frontback:
            self.position.z = value-collider_surface
        elif face in Face.updown:
            self.position.y = value-collider_surface
        self.update_surface(face)

    def on_collide(self, collision: Collision):
        self.on_collide_notify.notify(collision)

    
