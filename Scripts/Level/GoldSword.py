from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Level.SavePoint import SavePoint

from pygame import Vector3
from random import random
from Scripts.VFXManager.VFXManager import VFXManager
from Scripts.Attack.AttackParam import AttackParam
from Scripts.Attack.UnderAttackInterface import UnderAttackInterface
from Scripts.Animation.Animator import Animator
from Scripts.Locals import Tag, VFXID
from Scripts.Physics.RigidBody import RigidBody


class GoldSword(UnderAttackInterface):
    def __init__(self) -> None:
        super().__init__()
        self.savepoint: SavePoint = None
        self.rigidbody: RigidBody = None
        self.animator: Animator = None

        self.is_triggered = False

    def awake(self):
        self.rigidbody = self.get_component(RigidBody)
        self.animator = self.get_component(Animator)

    def under_attack(self, attack_param: AttackParam):
        if self.is_triggered:
            self.shake()
        elif attack_param.attacker.gameobject.compare_tag(Tag.player):
            self.savepoint.trigger()

    def trigger(self):
        self.is_triggered = True
        self.rigidbody.set_collider((45, 100, 20), (22.5, 0, 10))
        VFXManager.Instance().play(VFXID.goldsword_trigger,
                                   self.position+Vector3(0, 160, 10))
        self.animator.set_trigger("trigger")

    def shake(self):
        VFXManager.Instance().play(VFXID.goldsword_shake, self.position +
                                   Vector3(random()*100-50, random()*100+60, 10))
        self.animator.set_trigger("shake")

    def set_savepoint(self, savepoint: SavePoint):
        self.savepoint = savepoint
