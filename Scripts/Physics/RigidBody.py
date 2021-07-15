from __future__ import annotations
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.Collider import Collider
    from Scripts.Physics.Collision import Collision

from Scripts.Physics.Physics import Physics
from Scripts.GameObject.Component import Component
from Scripts.Locals import Face, ForceMode, GRAVITY
from pygame import Vector3

# TODO 完成RigidBody的類別圖


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

        self.on_collide_notify: list[Callable] = []

    # region setter

    def set_collider(self, collider: Collider):
        self.collider = collider

    def set_frozen(self, frozen: bool):
        self.frozen = frozen

    def set_damp(self, damp: float):
        self.damp = damp

    def set_apply_gravity(self, apply_gravity: bool):
        self.frozapply_gravityen = apply_gravity

    # endregion

    def start(self):
        Physics.attach(self)

    def end(self):
        Physics.detach(self)

    def update(self):
        # 更新物理
        if self.frozen:
            self.velocity *= 0
            return
        if self.apply_gravity:
            self.add_force(GRAVITY, ForceMode.force)
        self.velocity += self.acceleration
        self.velocity *= self.damp
        self.position += self.velocity*Physics.get_deltatime()  # 時間校正
        self.acceleration.xyz = (0, 0, 0)

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
            self.acceleration += force*Physics.get_deltatime()  # 時間校正
        if force_mode == ForceMode.impulse:
            self.acceleration += force

    def get_surface(self, face: Face):
        '''回傳碰撞箱(Collider)不同面的座標'''
        collider_surface = self.collider.get_surface(face)
        if face == Face.up or face == Face.down:
            return collider_surface+self.position.y
        if face == Face.right or face == Face.left:
            return collider_surface+self.position.x
        if face == Face.back or face == Face.front:
            return collider_surface+self.position.z

    def set_surface(self, face: Face, value: float):
        '''設定碰撞箱(Collider)不同面的座標，並改變位置(position)'''
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

    def on_collide(self, collision: Collision):
        self.notify(collision)

    def attach(self, func: Callable):
        '''
        註冊碰撞時想被通知的方法

        該方法應有一個碰撞資訊類別(Collision)的參數

        參考: def on_collide(collision: Collision)
        '''
        self.on_collide_notify.append(func)

    def detach(self, func: Callable):
        '''取消註冊碰撞時想被通知的方法'''
        if not func in self.on_collide_notify:
            raise Exception("detach the unkwon func!")
        self.on_collide_notify.remove(func)

    def notify(self, collision: Collision):
        '''通知註冊了碰撞事件的所有方法，並傳入碰撞資訊(Collision)'''
        for func in self.on_collide_notify:
            func(collision)
