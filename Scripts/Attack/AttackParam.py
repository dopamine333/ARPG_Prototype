from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character
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
    damage_text_dict:dict[int,dict[Tag,list[Image]]]={}
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
    def get_damage_text(self,damage:int,defender_tag:Tag):
        if damage in self.damage_text_dict:
            if defender_tag in self.damage_text_dict[damage]:
                return self.damage_text_dict[damage][defender_tag]

        color = (171, 3, 3) if defender_tag==Tag.player else (245, 255, 253)
        clip=[]
        for i in range(60):
            size=(i-60)*(-0.06 *i-0.7)
            #size=0.0025*(i-43.2)**3-1.461*(i-43.2)+55
            font = pygame.font.SysFont("Segoe Script", int(size*(self.damage*0.1+1)), True)
            text = font.render(str(self.damage), True, color)
            clip.append(Image(text))
        if not damage in self.damage_text_dict:
            self.damage_text_dict[damage]={}
        self.damage_text_dict[damage][defender_tag]=clip
        print("new text",damage,defender_tag)
        return self.damage_text_dict[damage][defender_tag]
    def show(self):
        damage_text = GameObject()
        #damage_text.add_component(LifeTimer).set_lifetime(2)
        animator=damage_text.add_component(Animator)
        render = damage_text.add_component(SpriteRender)
        animator.set_render(render)
        fading_away_animation=Animation()
        fading_away_animation.set_clip(self.get_damage_text(self.damage,self.defender.gameobject.tag))
        fading_away_animation.attach(59,damage_text.destroy)
        animator.set_default_animation(fading_away_animation)
        render.set_shadow_size((40, 40))
        position = \
            (self.attacker.position+self.defender.position)/2 \
            + Vector3(-25+random()*50, 90+random()*50, -25+random()*50)
        damage_text.set_position(position)
        damage_text.instantiate()
