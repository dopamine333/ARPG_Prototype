from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character
from random import random
from Scripts.Locals import Tag
from Scripts.Time.LifeTimer import LifeTimer
from Scripts.Graphic.Image import Image
from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.GameObject.GameObject import GameObject
from Scripts.Physics import RigidBody
from pygame import Color, Vector3
import pygame.font

# TODO 播放攻擊音效


class AttackParam:
    '''
    傳遞攻擊資訊

    並通知其他系統顯示攻擊資訊
    '''

    def __init__(self, damage: float, force: Vector3 = None) -> None:
        self.damage = damage
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
        color = (245, 255, 253) if self.attacker.compare_tag(
            Tag.player) else (250, 54, 0)
        font = pygame.font.SysFont("Segoe Script", self.damage*8+40, True)
        text = font.render(str(self.damage), True, color)
        damage_text = GameObject()
        damage_text_render = damage_text.add_component(SpriteRender)
        damage_text_render.set_image(Image(text))
        damage_text_render.set_shadow_size((40, 40))
        damage_text.add_component(LifeTimer).set_lifetime(2)
        damage_text_position = \
            (self.attacker.position+self.defender.position)/2 \
            + Vector3(-25+random()*50, 150+random()*50, 20+random()*50)
        damage_text.set_position(damage_text_position)
        damage_text.instantiate()
