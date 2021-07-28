from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character
from Scripts.VisualEffectManager.VisualEffectManager import VisualEffectManager
from Scripts.Animation.Animation import Animation
from Scripts.Animation.Animator import Animator
from random import random
from Scripts.Locals import Tag
from Scripts.Time.LifeTimer import LifeTimer
from Scripts.Graphic.Image import Image
from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.GameObject.GameObject import GameObject
from Scripts.Physics import RigidBody
from pygame import Color, Vector2, Vector3, image, mouse
import pygame.font

# TODO 播放攻擊音效


class AttackParam:
    '''
    傳遞攻擊資訊

    並通知其他系統顯示攻擊資訊
    '''
    damage_text_dict: dict[int, dict[Tag, list[Image]]] = {}

    def __init__(self, damage: int, force: Vector3 = None) -> None:
        self.damage = round(damage)
        if force:
            self.force = force
        else:
            self.force = Vector3()
        self.attacker: Character = None
        self.defender: Character = None

    def set_attacker(self, attacker: Character):
        self.attacker = attacker

    def set_defender(self, defender: Character):
        self.defender = defender
    # TODO 也許能做一個Timer，統一管理計時的類

    def show(self):
        position = (self.attacker.position+self.defender.position)/2 \
            + Vector3(-25+random()*50, 90+random()*50, -25+random()*50)
        VisualEffectManager.Instance().play_damagetext(
            self.damage, self.defender.gameobject.tag, position)
